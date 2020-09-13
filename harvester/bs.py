import requests
from bs4 import BeautifulSoup
import bs4
from pprint import pprint
import json
import re
import time
from urllib.parse import urlencode

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)


# base_url = "https://www.ncsasports.org"
# state_url = "https://www.ncsasports.org/athletic-scholarships/baseball/iowa"
# college_url = "https://www.ncsasports.org/athletic-scholarships/baseball/minnesota/itasca-community-college"
# college_url_2 = "https://www.ncsasports.org/athletic-scholarships/baseball/california/allan-hancock-college"
# delay = 60
# print('\n')


def download_college_data(university):
    college_url = university['college']['href']
    college = university['college']
    result = requests.get(college_url)
    content = result.content
    soup = BeautifulSoup(content, 'lxml')
    section_data_list = []

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
        pprint(array_of_sections)

    if (True):
        environment_section()

    print('________________________________________________')
    pprint(section_data_list)


obj = {
    "college": {
        "name": "Samford University",
        "address": "800 Lakeshore Dr, Birmingham, AL 35209, USA",
        "title": "Samford University Baseball Scholarships Guide",
        "image": "https://recruit-match.ncsasports.org/fasttrack/clientimages/15272college.jpg",
        "href": "https://www.ncsasports.org/athletic-scholarships/baseball/alabama/samford-university",
        "general_stat": [
            {"Division": "NCAA I"},
            {"Enrollment": "3266"},
            {"Type": "Private"},
            {"Setting": "Suburban"}
        ],
    }
}


download_college_data(obj)
