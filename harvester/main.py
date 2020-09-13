import os
import time
import sys
import json
import bs4
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
from urllib.parse import urlencode
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome("./chromedriver", options=chrome_options)
base_url = "https://www.ncsasports.org"
main_url = "https://www.ncsasports.org/athletic-scholarships/baseball"
delay = 60


def check_progress():
    try:
        f = open('map.json', 'r')
        f_read = f.read()
        f.close()
        f_loaded = json.loads(f_read)
        if (f_loaded['stages'].__len__() == 0):
            return 0
        else:
            for key, value in f_loaded["stages"].items():
                if(value == False):
                    return int(key)
            # if there is no false, send the last key
            return f_loaded["stages"].keys().__len__()
    except Exception as e:
        print("CANT A: ", e)
        print('creating map.json')
        obj = {"stages": {}}
        f = open('map.json', 'a')
        f.write(json.dumps(obj))
        f.close()
        return 0


def started_stage(stage):
    print(f'____started stage {stage}')
    f = open('map.json', 'r+')
    f_read = f.read()
    f_loaded = json.loads(f_read)
    if(f_loaded['stages'].__contains__(str(stage))):
        return
    else:
        f_loaded['stages'][stage] = False
        f.seek(0)
        f.truncate()
        f.close()
        f = open('map.json', 'w')
        f.write(json.dumps(f_loaded))


def finished_stage(stage):
    print(f'____finished stage {stage}')
    f = open('map.json', 'r+')
    f_read = f.read()
    f_loaded = json.loads(f_read)
    f_loaded['stages'].update({str(stage): True})
    f = open('map.json', 'w')
    f.write(json.dumps(f_loaded))


def construct_stage_0(prog):
    # create first layer for master.json
    started_stage(prog)
    state_result = requests.get(main_url)
    source_code = state_result.content
    soup = BeautifulSoup(source_code, 'lxml')
    links = soup.find_all('a')
    links = links[6:57]
    state_list = []
    link_count = 0
    for link in links:
        obj = {
            "state_id": link_count,
            "link": link.attrs['href'],
            "name": link.text,
            "data": {}
        }
        state_list.append(obj)
        f = open('master.json', 'w')
        f.write(json.dumps(state_list))
        link_count = link_count + 1
    f.close()
    finished_stage(prog)
    return prog + 1


def construct_stage_1(prog):
    # create a list of states that do have at least 1 league
    started_stage(prog)
    f = open('master.json', 'r')
    content = f.read()
    f.close()
    loaded_content = json.loads(content)
    start = 0
    for states in loaded_content:
        start = start + 1
        print("DOWNLOADING %", start / len(loaded_content))
        state_result = requests.get(states['link'])
        state_soup = BeautifulSoup(state_result.content, 'lxml')
        state_map_canvas = state_soup.find_all(id="map_canvas")
        if (len(state_map_canvas) == True):
            states.update({"hasLeague": True})
        else:
            states.update({"hasLeague": False})
    # update states in master.json with hasLeague
    f = open('master.json', 'w')
    data = json.dumps(loaded_content)
    f.write(data)
    f.close()
    finished_stage(prog)
    return prog + 1


def download_general_stat_map(obj):
    # download general data related to state
    result = requests.get(obj["link"])
    content = result.content
    soup = BeautifulSoup(content, 'lxml')
    # FOR SCHOOLS_OFFERING
    offerings = soup.find(id="schools_offering")
    # get title
    title = offerings.find("div").attrs['title']
    # get table and data
    table_data = []
    table_body = offerings.find_all("tr")
    for data in table_body:
        data = data.text.strip().split('\n')
        table_data.append(data)
    offerings_obj = {
        "title": title,
        "table_data": table_data
    }
    # +++++++
    scholarships = soup.find(id="scholarship_opportunities")
    title = scholarships.find("div").attrs['title']
    table_data = []
    table_body = scholarships.find_all("tr")
    for data in table_body:
        data = data.text.strip().split('\n')
        table_data.append(data)
    scholarships_obj = {
        "title": title,
        "table_data": table_data
    }
    # +++++++
    athlete_participation = soup.find(id="student_athlete_participation")
    title = athlete_participation.find("div").attrs['title']
    table_data = []
    table_body = athlete_participation.find_all("tr")
    for data in table_body:
        data = data.text.strip().split('\n')
        table_data.append(data)
    athlete_participation_obj = {
        "title": title,
        "table_data": table_data
    }

    #  package the general stats and return
    state_general_stats = {
        "offerings": offerings_obj,
        "scholarships": scholarships_obj,
        "participation": athlete_participation_obj
    }
    return state_general_stats


def download_list_of_colleges(obj):
    print('NOW HERE')
    driver.get(obj['link'])
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[3]")))
    except TimeoutException:
        print("Loading took too much time! on:", obj['name'])
        print('________________________________________')
    _src = myElem.get_attribute('innerHTML')
    soup = BeautifulSoup(_src, 'lxml')
    school_offerings = soup.find_all('div')
    school_offerings_range = len(school_offerings)
    list_of_colleges = []
    for i in range(1, school_offerings_range):
        download_percentage = (i / (school_offerings_range - 1))
        print(
            f'_____DOWNLOADING = {download_percentage}_______________')
        elem = driver.find_element_by_xpath(
            f'/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[3]/div[{i}]')
        driver.execute_script("arguments[0].click();", elem)
        try:
            data_console = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/div/div")))
        except TimeoutException:
            print("Loading took too much time! on:", obj['name'], "2nd")
        college_data = data_console.get_attribute('innerHTML')
        college_obj = {}
        college_data_soup = BeautifulSoup(college_data, 'lxml')
        # !!!!-----++
        college_obj["name"] = college_data_soup.find("a").text
        # !!!!-----++
        college_obj["address"] = college_data_soup.find(
            'div', {"class": "college_map_address"}).text
        # !!!!-----++
        college_obj["title"] = college_data_soup.find("a").attrs["title"]
        # !!!!-----++
        college_obj['image'] = college_data_soup.find("img").attrs["src"]
        # !!!!-----++
        href = college_data_soup.find("a").attrs["href"]
        college_obj['href'] = f'{base_url}{href}'
        # !!!!-----++
        stat_list = college_data_soup.find_all(
            'div', {"class": "college_map_stats"})
        college_stats = []
        for stat in stat_list:
            str_obj = {}
            str_array = stat.text.strip().split(":")
            str_obj[str_array[0].strip()] = str_array[1].strip()
            college_stats.append(str_obj)
        college_obj['general_stat'] = college_stats
        college_obj['data'] = {}  # for later use
        list_of_colleges.append(college_obj)

    print('________===_______')
    return list_of_colleges


def construct_stage_2(prog):
    started_stage(prog)
    try:
        f = open('stage_2_map.json', 'r')
        f.close()
    except FileNotFoundError as e:
        f = open('stage_2_map.json', 'a')
        f = open('stage_2_map.json', 'w')
        f.write(json.dumps([]))
        f.close()
        print('created stage_w_map.json ...')

    # create the stage 2 map
    try:
        first_count = 0
        # get the hasleauges = true states
        f = open('master.json', 'r')
        f_read = f.read()
        f.close()
        f_loaded_master = json.loads(f_read)
        listOf_hasLeauges = []
        for state in f_loaded_master:
            first_count = first_count + 1
            if (state['hasLeague'] == True):
                state_obj = {
                    "state_id": state['state_id'],
                    "link": state['link'],
                    "name": state['name'],
                    "isDownloaded": {
                        "general_stats": False,
                        "list_of_colleges": False,
                    }
                }
                listOf_hasLeauges.append(state_obj)
        # write the map for stage_2
        f = open("stage_2_map.json", "r")
        f_read_map = f.read()
        f_loaded_map = json.loads(f_read_map)
        for league in listOf_hasLeauges:
            f_loaded_map.append(league)
        data_dump = json.dumps(f_loaded_map)
        f = open('stage_2_map.json', 'w')
        f.write(data_dump)
        f.close()
        print(first_count / len(f_loaded_master))
    except Exception as e:
        print(e)

    # then
    # dowload the general data for state
    try:
        state_count = 0
        for state in listOf_hasLeauges:
            state_count = state_count + 1
            general_stat_of_state = []
            for key, value in state["isDownloaded"].items():
                if (value == False):
                    if (key == "general_stats"):
                        data_out = download_general_stat_map(state)
                        general_stat_of_state.append(data_out)
            # write the general data of state into master.json
            try:
                f = open('master.json', 'r')
                f_read = f.read()
                f.close()
                loaded_master = json.loads(f_read)
                _len = len(loaded_master)
                for _state in loaded_master:
                    if (_state['name'] == state['name']):
                        obj = {
                            "general_stats": general_stat_of_state
                        }
                        _state['data'].update(obj)
                        f = open('master.json', 'w')
                        f.write(json.dumps(loaded_master))
                        f.close()
                    # update the stage 2 map for general data
                        f = open("stage_2_map.json", "r")
                        f_read = f.read()
                        f_map_stage_2 = json.loads(f_read)
                        for item in f_map_stage_2:
                            if (item['name'] == _state['name']):
                                item['isDownloaded'].update(
                                    {"general_stats": True})
                                f = open('stage_2_map.json', 'w')
                                f.write(json.dumps(f_map_stage_2))
                                f.close()
                print(state_count / len(listOf_hasLeauges))
            except Exception as e:
                print("CANT: ", e)
    except Exception as e:
        print('here?')

    # then
    # download the list of colleges
    try:
        f = open("master.json", 'r')
        master = json.loads(f.read())
        f.close()
        state_count = 0
        list_of_colleges = []
        for state in listOf_hasLeauges:
            state_count = state_count + 1
            for key, value in state["isDownloaded"].items():
                if (value == False):
                    if (key == "list_of_colleges"):
                        # download the list
                        list_of_colleges = download_list_of_colleges(state)
            # write it to master for each state
            for obj in master:
                if (obj['name'] == state['name']):
                    f = open('master.json', 'w')
                    obj["data"].update({
                        "list_of_colleges": list_of_colleges
                    })
                    f.write(json.dumps(master))
                    f.close()
                    # update the stage 2 map satus for list of colleges
                    f = open("stage_2_map.json", "r")
                    f_read = f.read()
                    f_map_stage_2 = json.loads(f_read)
                    for item in f_map_stage_2:
                        if (item['name'] == obj['name']):
                            item['isDownloaded'].update(
                                {"list_of_colleges": True})
                            f = open('stage_2_map.json', 'w')
                            f.write(json.dumps(f_map_stage_2))
                            f.close()
            print(state_count, "/", len(listOf_hasLeauges))
        finished_stage(prog)
        return prog + 1
    except Exception as e:
        print("CANT: ", e)
        print('dont know yet')


def create_college_list_and_map():
    try:
        # create stage 3 map (college_main)
        f = open("stage_2_map.json", 'r')
        stage_2_map = json.loads(f.read())
        f.close()
        print("creating stage_3 map")
        f = open("master.json", 'r')
        f_loaded_master = json.loads(f.read())
        f.close()
        all_colleges = []
        count = 0
        for state in f_loaded_master:
            if (state['hasLeague'] == True):
                lon_lat_of_colleges_within_state = []
                print("for: ", state['name'])
                colleges = (state['data']['list_of_colleges'])
                for college in colleges:
                    print('  *', college["name"])
                    obj = {
                        "college_id": count,
                        "college": college,
                        "state": state['name'],
                        "isDownloaded": {
                            "general_info": False,
                            "athletics_section": False,
                            "admissions_section": False,
                            "environment_section": False,
                            "financial_section": False
                        }
                    }
                    all_colleges.append(obj)
                    lon_lat_of_colleges_within_state.append(
                        {"college_id": count, "downloaded": False})
                    count = count + 1
                for state_obj in stage_2_map:
                    if (state_obj["name"] == state['name']):
                        state_obj['isDownloaded'].update(
                            {"lon_lat": lon_lat_of_colleges_within_state, "state_lon_lat": False})
                f = open("stage_2_map.json", 'w')
                f.write(json.dumps(stage_2_map))
                f.close()
        r = open("college_list.json", 'w')
        college_list = json.dumps(all_colleges)
        r.write(college_list)
        r.close()

    except Exception as e:
        print("CANTx: ", e)


def construct_stage_3(prog):
    started_stage(prog)
    try:
        try:
            open('college_list.json', 'r')
        except Exception as e:
            print(e)
            open('college_list.json', 'a')
            f = open('college_list.json', 'w')
            f.write(json.dumps([]))
            f.close()
            print("created college_list.json")
        # create a list of all colleges
        try:
            create_college_list_and_map()
            finished_stage(prog)
            return prog + 1
        except Exception as e:
            print("CANTT: ", e)
    except Exception as e:
        print("CANT: construct_stage_3")
        print("CANT: ", e)


def download_college_data(university, section_to_download):
    college_url = university['college']['href']
    college = university['college']
    result = requests.get(college_url)
    content = result.content
    soup = BeautifulSoup(content, 'lxml')
    section_data_list = []

    def general_info_section():
        print("downloading general_info for", college['name'])
        # !!!!!!!
        college_name = soup.find('span', {"itemprop": "name"}).text
        # !!!!!!!
        college_street_address = soup.find(
            'span', {"itemprop": "streetAddress"}).text
        # !!!!!!!
        college_address_locality = soup.find(
            'span', {"itemprop": "addressLocality"}).text
        # !!!!!!!
        college_telephone = soup.find(
            'span', {"itemprop": "telephone"}).text
        # !!!!!!!
        college_official_website = soup.find("ul", {"itemprop": "address"})
        college_official_website = college_official_website.find('a').text
        # !!!!!!!
        profile_overview = soup.find('dl', {'class': "profile-overview"})
        over_view_elems = []
        for overview in profile_overview:
            if (type(overview) == bs4.element.Tag):
                over_view_elems.append(overview.text)
        over_view_len = len(over_view_elems)
        new_over_view_elems = []
        for i in range(0, over_view_len):
            listed = list(over_view_elems[i])
            new_string = []
            skip = False
            for letter in listed:
                if (skip == True):
                    skip = False
                else:
                    if (letter == '\\'):
                        skip = True
                    else:
                        new_string.append(letter)
            new_over_view_elems.append(''.join(new_string))
        cleaned_over_view = []
        for i in new_over_view_elems:
            cleaned_over_view.append(" ".join(i.split()))
        college_over_view = []
        for i in range(0, len(cleaned_over_view)):
            if ((i % 2) == 0):
                college_over_view.append(
                    [cleaned_over_view[i], cleaned_over_view[i+1]])
        # !!!!!!!
        data = {
            "name": college_name,
            "street_address": college_street_address,
            "address_locality": college_address_locality,
            "tel": college_telephone,
            "official_website": college_official_website,
            "overview": college_over_view
        }
        # store to heap
        section_data_list.append({"general_info": data})

    def athletics_section():
        print("downloading athletics_section")
        athletics_section = soup.find('div', {"id": "summary_cont"})
        all_sections = athletics_section.find_all('section')
        section_master = []
        for section in all_sections:
            if(len(section) == 5):
                temp_list = section.text.split('\n')
                header = temp_list[1]
                temp_body = temp_list[3:len(temp_list)]
                obj = {
                    f"{header}": temp_body
                }
                section_master.append(obj)
        section_data_list.append({"athletics_section": section_master})

    def admissions_section():
        def cleanUp(textString, stage):
            textString = textString.replace('\n', ',')
            textString = re.sub(' +', ' ', f'{textString}')
            textString = (textString.split(','))
            if (stage == 5):
                if (len(textString) > 1):
                    package = []
                    for i in range(1, len(textString) - 1):
                        if (i % 2 != 0):
                            package.append([textString[i], textString[i+1]])
                    return package
            if (stage == 7):
                package = {}
                temp_list = []
                for i in range(1, len(textString) - 1):
                    if (i == 1):
                        package.update({'title': textString[i]})
                    if (i % 2 != 1):
                        temp_list.append([textString[i], textString[i+1]])
                package.update({'body': temp_list})
                return package
            if (stage == 13):
                package = {}
                temp_list = []
                for i in range(1, len(textString) - 1):
                    if (i == 1):
                        package.update({'title': textString[i]})
                    else:
                        temp_list.append(textString[i])
                package.update({'body': temp_list})
                return package
            return []
        print("downloading admissions_section")
        admissions_section = soup.find('div', {"id": "admissions_cont"})
        all_sections = admissions_section.find_all('section')
        micro_section_list = []
        for section in all_sections:
            if (len(section) == 5):
                micro_section = {}
                for micro in section:
                    if(type(micro) == bs4.element.Tag):
                        if (vars(micro)['name'] == 'h6'):
                            # clean up // add as header
                            title = micro.text
                            micro_section.update({
                                'header': title,
                            })
                        else:
                            # clean up// add as body
                            body = cleanUp(micro.text, 5)
                            micro_section.update({
                                'body': body,
                            })
                micro_section_list.append(micro_section)

            if (len(section) == 7):
                micro_section = {}
                for micro in section:
                    if(type(micro) == bs4.element.Tag):
                        if (len(micro) == 1):
                            micro_section.update(
                                {'header': micro.text, "body": {}})
                        else:
                            body = cleanUp(micro.text, 7)
                            micro_section['body'].update({
                                f'{body["title"]}': body['body']
                            })
                micro_section_list.append(micro_section)
                print('\n')
            if (len(section) == 13):
                micro_section = {}
                for micro in section:
                    if(type(micro) == bs4.element.Tag):
                        if(len(micro) == 1):
                            micro_section.update(
                                {'header': micro.text, "body": {}})
                        else:
                            body = cleanUp(micro.text, 13)
                            micro_section['body'].update({
                                f'{body["title"]}': body['body']
                            })
                micro_section_list.append(micro_section)
        section_data_list.append({"admissions_section": micro_section_list})

    def environment_section():
        print("downloading environment_section")
        environment_section = soup.find('div', {"id": "environment_cont"})
        all_sections = environment_section.find_all('section')
        array_of_sections = []
        for section in all_sections:
            micro_list = {}
            for micro in section:
                if(type(micro) == bs4.element.Tag):
                    if (vars(micro)['name'] == 'h6'):
                        micro_list.update({'header': micro.text})
                    else:
                        mini_array = []
                        for mini in micro:

                            if(type(mini) == bs4.element.Tag):
                                mini_array.append(mini.text)
                            else:
                                if (micro_list['header'] == "Location Description:"):
                                    text = mini.replace(
                                        '\n', ',').replace('\t', ',')
                                    text = re.sub(' +', ' ', f'{text}')
                                    mini_array.append(text)

                        micro_list.update({'body': mini_array})
            array_of_sections.append(micro_list)
        section_data_list.append({"environment_section": array_of_sections})

    def financial_section():
        print("downloading financial_section")
        financial_section = soup.find('div', {"id": "financial_cont"})
        all_sections = financial_section.find_all('section')
        micro_section_list = []
        for section in all_sections:
            lil_section = {}
            if (len(section) == 5):
                section_5 = []
                for micro in section:
                    if(type(micro) == bs4.element.Tag):
                        if (vars(micro)['name'] == 'h6'):
                            lil_section.update({
                                'header': micro.text,
                            })
                        if (len(micro) > 5):
                            for tiny in micro:
                                if(type(tiny) == bs4.element.Tag):
                                    section_5.append(tiny.text)
                lil_section.update({"body": section_5})
                micro_section_list.append(lil_section)
            if (len(section) == 9):
                section_9 = []
                for micro in section:
                    if(type(micro) == bs4.element.Tag):
                        if (vars(micro)['name'] == 'h6'):
                            lil_section.update({
                                'header': micro.text,
                            })
                    if(type(micro) == bs4.element.Tag):
                        for tiny in micro:
                            if(type(tiny) == bs4.element.Tag):
                                text = tiny.text.replace(
                                    '\n', ',').replace('\t', ',')
                                text = re.sub(' +', ' ', f'{text}')
                                section_9.append(text)
                lil_section.update({"body": section_9})
                micro_section_list.append(lil_section)
        section_data_list.append({"financial_section": micro_section_list})

    if (section_to_download == "general_info"):
        general_info_section()

    if (section_to_download == "athletics_section"):
        athletics_section()

    if (section_to_download == "admissions_section"):
        admissions_section()

    if (section_to_download == "environment_section"):
        environment_section()
    if (section_to_download == "financial_section"):
        financial_section()

    print('________________________________________________')
    return section_data_list


def construct_stage_6(prog):
    try:
        # download the data-section of each collge
        started_stage(prog)
        r = open('college_list.json', "r")
        college_list = json.loads(r.read())
        r.close()
        total_count = 0
        for college in college_list:
            print("NEXT college...", college["college"]['name'])
            list_of_sections_to_download = []
            for key, value in college['isDownloaded'].items():
                if (value == False):
                    list_of_sections_to_download.append(key)
            section_count = 0
            for section in list_of_sections_to_download:
                data = download_college_data(college, section)
                section_count += 1
                print("%", (section_count / len(list_of_sections_to_download)) * 100, "DOWNLOADED:", section, 'for',
                      college["college"]['name'])

                college['college']['data'].update({
                    f"{section}": data[0]
                })
                college['isDownloaded'].update({
                    f"{section}": True
                })

                r = open('college_list.json', "w")
                r.write(json.dumps(college_list))
                r.close()
                print('%', (total_count / len(college_list)) * 100, '--> TOTAL')
            total_count += 1

        finished_stage(prog)
        return prog + 1
    except Exception as e:
        print(e)


def getLonLan(address):
    try:
        google_api_key = "AIzaSyBwJMRswlAhHuhEi3lVQQfSGDFsWJwjyNo"
        data_type = 'json'
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
        params = {"address": address,
                  "key": google_api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            print('bad satus code for:', address)
        else:
            obj = r.json()
            obj_result = obj['results'][0]
            formatted_address = obj_result['formatted_address']
            lon_lat = obj_result['geometry']['location']
            location = {
                "formatted_address": formatted_address,
                "lon_lat": lon_lat
            }
            return location
    except Exception as e:
        print(e)


def construct_stage_5(prog):
    started_stage(prog)
    # download lon lat
    try:
        f = open("stage_2_map.json", 'r')
        stage_2_map = json.loads(f.read())
        f.close()
        f = open("master.json", 'r')
        master = json.loads(f.read())
        f.close()
        for state_map in stage_2_map:
            if(state_map['isDownloaded']['state_lon_lat'] == False):
                state_name = state_map['name']
                for state in master:
                    if(state_name == state['name']):
                        print('lon - lan:', state['name'])
                        state_location = getLonLan(state_name)
                        state.update({"lonlat": state_location['lon_lat']})
                        state.update(
                            {"address": state_location['formatted_address']})
                        f = open("master.json", 'w')
                        f.write(json.dumps(master))
                        f.close()

                        state_map['isDownloaded'].update(
                            {"state_lon_lat": True})
                        f = open("stage_2_map.json", 'w')
                        f.write(json.dumps(stage_2_map))
                        f.close()
    except Exception as e:
        print('5 A', e)

    try:
        f = open("stage_2_map.json", 'r')
        stage_2_map = json.loads(f.read())
        f.close()
        f = open("master.json", 'r')
        master = json.loads(f.read())
        f.close()
        for state_map in stage_2_map:
            list_of_uni_map = state_map['isDownloaded']["lon_lat"]
            for college_map in list_of_uni_map:
                if (college_map['downloaded'] == False):
                    for state in master:
                        if (state_map['name'] == state['name']):
                            for college in state['data']['list_of_colleges']:
                                if (college['college_id'] == college_map['college_id']):
                                    print('lon-lat for: ',
                                          college['college_id'], college['name'])
                                    college_name = college['name']
                                    college_address = college['address']
                                    forGeoCode = college_name + ' ' + college_address
                                    college_location = getLonLan(forGeoCode)
                                    college.update(
                                        {"lonlat": college_location['lon_lat']})
                                    college.update(
                                        {"address": college_location['formatted_address']})
                                    f = open("master.json", 'w')
                                    f.write(json.dumps(master))
                                    f.close()

                                    college_map.update(
                                        {"downloaded": True})
                                    f = open("stage_2_map.json", 'w')
                                    f.write(json.dumps(stage_2_map))
                                    f.close()

        finished_stage(prog)
        return prog + 1

    except Exception as e:
        print('5 B', e)


def construct_stage_4(prog):
    started_stage(prog)
    try:
        f = open('master.json', 'r')
        master = json.loads(f.read())
        f.close()
        college_count = 0
        for state in master:
            if(state['hasLeague'] == True):
                for college in state['data']['list_of_colleges']:
                    college.update({'college_id': college_count})
                    college_count = college_count + 1
        f = open("master.json", 'w')
        f.write(json.dumps(master))
        f.close()
        finished_stage(prog)
        return prog + 1
    except Exception as e:
        print(e)


def construct_stage_7(prog):
    started_stage(prog)
    try:
        f = open('master.json', 'r')
        master = json.loads(f.read())
        f.close()
        f = open('college_list.json', 'r')
        college_list = json.loads(f.read())
        f.close()

        for state in master:
            if(state['hasLeague'] == True):
                for college in state['data']['list_of_colleges']:
                    address = college['address']
                    college_id = college['college_id']
                    lonlat = college['lonlat']
                    for colle in college_list:
                        if (college_id == colle["college_id"]):
                            colle['college'].update({"address": address})
                            colle['college'].update({"lonlat": lonlat})
                            print('updated college id: ', college_id)
        f = open('college_list.json', 'w')
        f.write(json.dumps(college_list))
        f.close()
        finished_stage(prog)
        return prog + 1
    except Exception as e:
        print('7 A', e)


def main():
    prog = check_progress()
    total_stages = 8
    print(f'@ prog: {prog} /', total_stages)

    if (prog == 0):
        prog = construct_stage_0(prog)

    if (prog == 1):
        prog = construct_stage_1(prog)

    if (prog == 2):
        prog = construct_stage_2(prog)

    if (prog == 3):
        prog = construct_stage_3(prog)

    if (prog == 4):
        prog = construct_stage_4(prog)

    if (prog == 5):
        prog = construct_stage_5(prog)

    if (prog == 6):
        prog = construct_stage_6(prog)

    if (prog == 7):
        prog = construct_stage_7(prog)

    driver.close()
    print(f'@ prog: {prog} /', total_stages)
    print('''
          Done done...
          Have a good day
          <3 :)
          ''')


if __name__ == "__main__":
    main()
