

# def construct_stage_6():
#     ex_state_name = 'Alabama'
#     ex_adress = "Thousand Oaks, 60 W Olsen Rd"

#     google_api_key = "AIzaSyBwJMRswlAhHuhEi3lVQQfSGDFsWJwjyNo"
#     data_type = 'json'
#     endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
#     params = {"address": ex_state_name,
#               "key": google_api_key}
#     url_params = urlencode(params)
#     url = f"{endpoint}?{url_params}"
#     response = requests.get(url)
#     obj = response.json()

#     obj_result = obj['results'][0]
#     formatted_address = obj_result['formatted_address']
#     lon_lat = obj_result['geometry']['location']

#     print(formatted_address, lon_lat)

# formatted_address = obj_result["formatted_address"]
# lon_lat = obj_result['geometry']['location']

# pprint(formatted_address, lon_lat)


# construct_stage_6()


# def construct_stage_5():
#     f = open("master.json", 'r')
#     f2 = open("college_list.json", 'r')
#     master = json.loads(f.read())
#     college_list = json.loads(f2.read())
#     f.close()
#     f2.close()
#     college_count = 0
#     for state in master:
#         if (state["hasLeague"] == True):
#             len_of_college_list = len(state["data"]["list_of_colleges"])
#             for i in range(0, len_of_college_list):
#                 current_college = state["data"]["list_of_colleges"][i]
#                 current_college.update({"id": college_count})
#                 college_count += 1
#                 f = open("master.json", 'w')
#                 f.write(json.dumps(master))
#                 f.close()
#                 print('_+_+_+_')
#                 time.sleep(2)


# construct_stage_5()


# result = requests.get(college_url)
# result_2 = requests.get(college_url_2)

# content = result.content
# content_2 = result_2.content

# soup = BeautifulSoup(content, 'lxml')
# soup_2 = BeautifulSoup(content_2, 'lxml')

# soup_list = [soup, soup_2]

# for soup in soup_list:
#     def cleanUp(textString, stage):
#         textString = textString.replace('\n', ',')
#         textString = re.sub(' +', ' ', f'{textString}')
#         textString = (textString.split(','))
#         if(stage == 5):
#             package = []
#             for i in range(1, len(textString) - 1):
#                 if (i % 2 != 0):
#                     package.append([textString[i], textString[i+1]])
#             return package
#         return []
#     financial_section = soup.find('div', {"id": "financial_cont"})
#     all_sections = financial_section.find_all('section')
#     micro_section_list = []
#     for section in all_sections:
#         if (len(section) == 5):
#             micro_section = {}
#             for micro in section:
#                 if(type(micro) == bs4.element.Tag):
#                     if (vars(micro)['name'] == 'h6'):
#                         # clean up // add as header
#                         micro_section.update({
#                             'header': micro.text,
#                         })
#                     else:
#                         body = cleanUp(micro.text, 5)
#                         micro_section.update({
#                             'body': body,
#                         })
#             micro_section_list.append(micro_section)

#         if (len(section) == 9):
#             section = section.text.split('\n')
#             header = section[1]
#             ref = [section[2], section[3]]
#             body = section[6:len(section)]

#             new_body_list = []
#             for item in body:
#                 textString = item.replace('\t', ' ')
#                 textString = re.sub(' +', ' ', f'{textString}')
#                 if (len(textString) > 1):
#                     new_body_list.append(textString)
#             # package the body
#             packaged_by_3 = {}
#             count = 0
#             for i in range(0, len(new_body_list) - 2):
#                 if (count == 0):
#                     count + 1
#                     packaged_by_3.update({
#                         f'{new_body_list[i]}': [new_body_list[i+1], new_body_list[i+2]]
#                     })
#                 if (count == 3):
#                     count = 0
#             obj = {
#                 f"{header}": packaged_by_3,
#                 "ref": ref
#             }
#             micro_section_list.append(obj)

#     print(micro_section_list)
#     print('_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_')

# def cleanUp(textString, stage):
#     textString = textString.replace('\n', ',')
#     textString = re.sub(' +', ' ', f'{textString}')
#     textString = (textString.split(','))
#     if (stage == 5):
#         if (len(textString) > 1):
#             package = []
#             for i in range(1, len(textString) - 1):
#                 if (i % 2 != 0):
#                     package.append([textString[i], textString[i+1]])
#             return package
#     if (stage == 7):
#         package = {}
#         temp_list = []
#         for i in range(1, len(textString) - 1):
#             if (i == 1):
#                 package.update({'title': textString[i]})
#             if (i % 2 != 1):
#                 temp_list.append([textString[i], textString[i+1]])
#         package.update({'body': temp_list})
#         return package
#     if (stage == 13):
#         package = {}
#         temp_list = []
#         for i in range(1, len(textString) - 1):
#             if (i == 1):
#                 package.update({'title': textString[i]})
#             else:
#                 temp_list.append(textString[i])
#         package.update({'body': temp_list})
#         return package
#     return []
# admissions_section = soup.find('div', {"id": "admissions_cont"})
# all_sections = admissions_section.find_all('section')
# micro_section_list = []
# for section in all_sections:
#     if (len(section) == 5):
#         micro_section = {}
#         for micro in section:
#             if(type(micro) == bs4.element.Tag):
#                 if (vars(micro)['name'] == 'h6'):
#                     # clean up // add as header
#                     title = micro.text
#                     micro_section.update({
#                         'header': title,
#                     })
#                 else:
#                     # clean up// add as body
#                     body = cleanUp(micro.text, 5)
#                     micro_section.update({
#                         'body': body,
#                     })
#         micro_section_list.append(micro_section)

#     if (len(section) == 7):
#         micro_section = {}
#         for micro in section:
#             if(type(micro) == bs4.element.Tag):
#                 if (len(micro) == 1):
#                     micro_section.update(
#                         {'header': micro.text, "body": {}})
#                 else:
#                     body = cleanUp(micro.text, 7)
#                     micro_section['body'].update({
#                         f'{body["title"]}': body['body']
#                     })
#         micro_section_list.append(micro_section)
#         print('\n')
#     if (len(section) == 13):
#         micro_section = {}
#         for micro in section:
#             if(type(micro) == bs4.element.Tag):
#                 if(len(micro) == 1):
#                     micro_section.update(
#                         {'header': micro.text, "body": {}})
#                 else:
#                     body = cleanUp(micro.text, 13)
#                     micro_section['body'].update({
#                         f'{body["title"]}': body['body']
#                     })
#         micro_section_list.append(micro_section)
# pprint(micro_section_list)


# def admissions_section():
#     def cleanUp(textString):
#         textString = textString.replace('\n', ',')
#         textString = re.sub(' +', ' ', f'{textString}')
#         textString = (textString.split(','))
#         if (len(textString) > 1):
#             new_list = []
#             cleaned_list = []
#             for item in textString:
#                 if (len(item) > 0):
#                     cleaned_list.append(item)
#             for i in range(0, len(cleaned_list)):
#                 if ((i % 2) == 0):
#                     new_list.append([cleaned_list[i], cleaned_list[i+1]])
#                 # print(new_list)
#             return new_list
#         return textString
#     print("downloading admissions_section")
#     admissions_section = soup.find('div', {"id": "admissions_cont"})
#     all_sections = admissions_section.find_all('section')
#     micro_section_list = []
#     for section in all_sections:
#         if (len(section) == 5):
#             micro_section = {}
#             for micro in section:
#                 if(type(micro) == bs4.element.Tag):
#                     if (vars(micro)['name'] == 'h6'):
#                         # clean up // add as header
#                         title = cleanUp(micro.text)
#                         micro_section.update({
#                             'header': title,
#                         })
#                     else:
#                         # clean up// add as body
#                         body = cleanUp(micro.text)
#                         micro_section.update({
#                             'body': body,
#                         })
#             micro_section_list.append(micro_section)
#         # @@@@@@@@
#         if (len(section) == 7):
#             micro_section = {}
#             body_section = {}
#             for micro in section:
#                 if(type(micro) == bs4.element.Tag):
#                     if (vars(micro)['name'] == 'h6'):
#                         header = cleanUp(micro.text)
#                         micro_section.update({
#                             'header': header,
#                         })
#                     else:
#                         # body = cleanUp(micro.text)
#                         temp_list = micro.text.split('\n')
#                         new_temp = []
#                         for li in temp_list:
#                             if (len(li) == 0):
#                                 print('\n')
#                             else:
#                                 new_temp.append(li)
#                         header = new_temp[0]
#                         body = new_temp[1:len(new_temp)]
#                         body = ",".join(body)
#                         body = cleanUp(body)
#                         body_section.update({
#                             f'{header}': body
#                         })
#                 micro_section.update({
#                     "body": body_section
#                 })
#             micro_section_list.append(micro_section)
#         # @@@@@@@@
#         if (len(section) == 13):
#             micro_section = {}
#             body_section = {}
#             for micro in section:
#                 if(type(micro) == bs4.element.Tag):
#                     if (len(micro) == 1):
#                         header = cleanUp(micro.text)
#                         micro_section.update({
#                             'header': header,
#                         })
#                     if (len(micro) == 5):
#                         header = micro.find('h6').text
#                         micro_section_body = micro.find('li').text
#                         body_section.update({
#                             f"{header}": micro_section_body
#                         })
#                         micro_section.update({
#                             "body": body_section
#                         })
#                     if (len(micro) > 5):
#                         temp_list = micro.text.split("\n")
#                         new_list = []
#                         for item in temp_list:
#                             if (len(item) > 3):
#                                 new_list.append(item)
#                         header = new_list[0]
#                         micro_section_body = new_list[1:len(new_list)]
#                         body_section.update({
#                             f"{header}": micro_section_body
#                         })
#                         micro_section.update({
#                             "body": body_section
#                         })
#             micro_section_list.append(micro_section)
#     section_data_list.append({"admissions_section": micro_section_list})


# admission = soup.find('div', {"id": "admissions_cont"})
# admission_2 = soup_2.find('div', {"id": "admissions_cont"})
# print('\n')
# print('\n')
# pprint('_____________________________________')


# all_sections = admission.find_all('section')

# for section in all_sections:
#     pprint(len(section))
#     print('\n')
#     micro_section_list = []
#         for section in all_sections:
#             if (len(section) == 5):
#                 micro_section = {}
#                 for micro in section:
#                     if(type(micro) == bs4.element.Tag):
#                         if (vars(micro)['name'] == 'h6'):
#                             # clean up // add as header
#                             title = cleanUp(micro.text)
#                             micro_section.update({
#                                 'header': title,
#                             })
#                         else:
#                             # clean up// add as body
#                             body = cleanUp(micro.text)
#                             micro_section.update({
#                                 'body': body,
#                             })
#                 micro_section_list.append(micro_section)
#             # @@@@@@@@
#             if (len(section) == 7):
#                 micro_section = {}
#                 body_section = {}
#                 for micro in section:
#                     if(type(micro) == bs4.element.Tag):
#                         if (vars(micro)['name'] == 'h6'):
#                             header = cleanUp(micro.text)
#                             micro_section.update({
#                                 'header': header,
#                             })
#                         else:
#                             # body = cleanUp(micro.text)
#                             temp_list = micro.text.split('\n')
#                             new_temp = []
#                             for li in temp_list:
#                                 if (len(li) == 0):
#                                     print('\n')
#                                 else:
#                                     new_temp.append(li)
#                             header = new_temp[0]
#                             body = new_temp[1:len(new_temp)]
#                             body = ",".join(body)
#                             body = cleanUp(body)
#                             body_section.update({
#                                 f'{header}': body
#                             })
#                     micro_section.update({
#                         "body": body_section
#                     })
#                 micro_section_list.append(micro_section)
#             # @@@@@@@@
#             if (len(section) == 13):
#                 micro_section = {}
#                 body_section = {}
#                 for micro in section:
#                     if(type(micro) == bs4.element.Tag):
#                         if (len(micro) == 1):
#                             header = cleanUp(micro.text)
#                             micro_section.update({
#                                 'header': header,
#                             })
#                         if (len(micro) == 5):
#                             header = micro.find('h6').text
#                             micro_section_body = micro.find('li').text
#                             body_section.update({
#                                 f"{header}": micro_section_body
#                             })
#                             micro_section.update({
#                                 "body": body_section
#                             })
#                         if (len(micro) > 5):
#                             temp_list = micro.text.split("\n")
#                             new_list = []
#                             for item in temp_list:
#                                 if (len(item) > 3):
#                                     new_list.append(item)
#                             header = new_list[0]
#                             micro_section_body = new_list[1:len(new_list)]
#                             body_section.update({
#                                 f"{header}": micro_section_body
#                             })
#                             micro_section.update({
#                                 "body": body_section
#                             })
#                 micro_section_list.append(micro_section)
#         section_data_list.append({"admissions_section": micro_section_list})

#     # time.sleep(2)

#     # pprint(section)
#     print('********************************')


# pprint('+++++++++++++++++++++++++++++++++++++')
# pprint('+++++++++++++++++++++++++++++++++++++')
# pprint('+++++++++++++++++++++++++++++++++++++')
# print('\n')
# pprint('+++++++++++++++++++++++++++++++++++++')
# pprint('+++++++++++++++++++++++++++++++++++++')
# pprint('+++++++++++++++++++++++++++++++++++++')


# all_sections_2 = admission_2.find_all('section')
# for section in all_sections_2:
#     pprint(len(section))
#     print('\n')
#     # time.sleep(2)
#     # pprint(section)
#     print('********************************')

# pprint('_____________________________________')
# print('\n')
# print('\n')


# def construct_stage_4(prog):
#     try:
#         # download the data-section of each collge
#         r = open('college_list.json', "r")
#         college_list = json.loads(r.read())
#         r.close()
#         total_count = 0
#         for college in college_list:
#             print("NEXT college...", college["college"]['name'])
#             list_of_sections_to_download = []
#             for key, value in college['isDownloaded'].items():
#                 if (value == False):
#                     list_of_sections_to_download.append(key)
#             section_count = 0
#             for section in list_of_sections_to_download:
#                 # data = download_college_data(college, section)
#                 print("______DOWNLOADED:", section, 'for',
#                       college["college"]['name'], section_count / len(list_of_sections_to_download), 'TOTAL: ', total_count / len(college_list))
#                 for i, item in enumerate(college['college']['data']):
#                     if item
#                 college['college']['data'][0].update({
#                     f"{section}": data
#                 })
#                 college['isDownloaded'].update({
#                     f"{section}": True
#                 })

#                 pprint(college_list)
#                 # r = open('college_list.json', "w")
#                 # r.write(json.dumps(college_list))
#                 # r.close()
#             total_count += 1

#         # finished_stage(prog)
#         # return prog + 1
#     except Exception as e:
#         print(e)


# def construct_stage_4(prog):
#     try:
#         # download the data-section of each collge
#         started_stage(prog)
#         r = open('college_list.json', "r")
#         college_list = json.loads(r.read())
#         r.close()
#         total_count = 0
#         for college in college_list:
#             list_of_sections_to_download = []
#             for key, value in college['isDownloaded'].items():
#                 if (value == False):
#                     list_of_sections_to_download.append(key)
#             data = download_college_data(college, list_of_sections_to_download)
#             print("______DOWNLOADED:",
#                   college["college"]['name'], total_count / len(college_list))
#             college['college'].update({
#                 "data": data
#             })
#             r = open('college_list.json', "w")
#             r.write(json.dumps(college_list))
#             r.close()
#             total_count = total_count + 1
#             print("_____WROTE:", college["college"]
#                   ['name'], total_count / len(college_list))
#         finished_stage(prog)
#         return prog + 1
#     except Exception as e:
#         print(e)


#             for college in college_list:
#             print("NEXT college...", college["college"]['name'])
#             list_of_sections_to_download = []
#             for key, value in college['isDownloaded'].items():
#                 if (value == False):
#                     list_of_sections_to_download.append(key)
#             section_count = 0
#             for section in list_of_sections_to_download:
#                 data = download_college_data(college, section)
#                 print("______DOWNLOADED:", section, 'for',
#                       college["college"]['name'], section_count / len(list_of_sections_to_download), 'TOTAL: ', total_count / len(college_list))
#                 for i, item in enumerate(college['college']['data']):
#                     if item

# pprint(college)
#     list_of_sections_to_download = []
#     for key, value in college['isDownloaded'].items():
#         if (value == False):
#             list_of_sections_to_download.append(key)
#     data = download_college_data(college, list_of_sections_to_download)
#     print("______DOWNLOADED:",
#           college["college"]['name'], total_count / len(college_list))
#     college['college'].update({
#         "data": data
#     })
#     r = open('college_list.json', "w")
#     r.write(json.dumps(college_list))
#     r.close()
#     total_count = total_count + 1
#     print("_____WROTE:", college["college"]
#           ['name'], total_count / len(college_list))
# finished_stage(prog)
# return prog + 1
#     except Exception as e:
#         print(e)


# construct_stage_4(4)


# result = requests.get(college_url)
# content = result.content

# f = open('test.txt', "r")
# f_read = f.read()
# f.close()
# content = f_read

# soup = BeautifulSoup(content, 'lxml')
# athletics_section = soup.find('div', {"id": "summary_cont"})
# admission = soup.find('div', {"id": "summary_cont"})
# environment = soup.find('div', {"id": "summary_cont"})
# financial = soup.find('div', {"id": "summary_cont"})


# all_sections = athletics_section.find_all('section')
# section_master = []
# for i in range(0, len(all_sections)):
#     try:
#         def cleanUp(textString):
#             textString = textString.replace('\\n', ',')
#             textString = re.sub(' +', ' ', f'{textString}')
#             textString = (textString.split(','))
#             section_obj = {}
#             text_list = []
#             body = []
#             for text in textString:
#                 if (len(text) > 1):
#                     text_list.append(text)

#             for i in range(0, len(text_list)):
#                 round = i - 1
#                 if (i == 0):
#                     section_obj['header'] = text_list[i]
#                 else:
#                     if (round % 2 == 0):
#                         body.append({text_list[i]: text_list[i + 1]})
#             section_obj['body'] = body
#             return section_obj
#         section = all_sections[i]
#         section_obj = cleanUp(section.text)
#         section_master.append(section_obj)
#     except:
#         print('\n cant create section object')  # no h6

# pprint({"athletics_section": section_master})


#         for i in range(0, all_sections.__len__()):

#             obj_body = [
#                 {"title": 22}
#             ]
#             print(section)
# section_obj["body"] = obj_body
# table = all_sections[i]
# if (table.find('h6') != None):
# groups = table.text
# cleaned_groups = cleanUp(groups)

# print(cleaned_groups)

# clean_tables = []
# x = cleanUp(table.text)
# cleaned_data = cleanUp(table.text)
# obj_body = packUp(cleaned_data)
# print(section_obj)
# print('+++___++++')
# print('+++___++++')
# print('+++___++++')
# print('+++___++++')
# print('+++___++++')
# print('+++___++++')
# print('+++___++++')

# body = [
#   {

#     "athletics" :
#   }
# ]
# obj = {
#   "header" : header
# }
# for section in good_sections:
#     for elem in section:
#         if (type(elem) == bs4.element.Tag):
#             header = None
#             body = None
#             if(vars(elem)['name'] == 'h6'):
#                 header = elem.text
#             else:

#                 def end():
#                     print("___+++___+++___")

#                 def cleanUp():
#                     # print("@@", textString)
#                     textString = textString.replace('\\n', '')
#                     textString = re.sub(' +', ' ', f'{textString}')
#                     # print(textString)
#                     return textString

# print(elem)
# tags_list = []
# for tags in elem:
# if (type(tags) == bs4.element.Tag):
# tags_list.append(tags)
# print(tags_list[0])
# end()

# print('#@')
# cleaned_tags = []
# end()
# end()
# print("tags")
# print(type(tags))
# print(tags)
# print(cleanUp(tags, 'tags'))
# text = cleanUp(tags.text)
# print(text)

# clean up
# print(tags)
# content.append(text)
# print(text)
# end()
# end()
# end()
# make package with content
# content_len = len(content)
# print(content_len)
# for i in range(0, content_len):
# if ((i % 2) == 0):
# print(content[i], content[i+1])
# obj = {
# f'{content[0]}'
# }
# print(content[0])
# for i in range(0, content_len):
#     # print(dir(content[i]))
#     obj = {
#         f'{content[i]}':}
#     print()
# end()
# for content_len
# print(content[0], content[1],content[0], content[1])
# end()
# package = [content[0], content[1]]
# print(package)
# for i in content:
#     package_name = f'stage_3_{content_len}.json'
#     f = open(package_name, 'a+')
# f.write(str(i))
# print(content_len)
# print(i)

# for i in range(0, content_len):
# for i in range(0, content_len):
# print(content[i], content[i+1])
# end()
# if (count % 2 == 0):
# print(content[i], content[i+1])
# count = count + 1
# end()
# end()
# end()
# end()

# for i in content:
# print(i)
# for section in good_sections:
#     header = section.find('h6', {"class": "m-section-title"}).text
#     information_body = []
#     body = section.find("dl", {"class": "profile-overview"})
#     body_2 = []
#     for i in body:
#         if (type(i) == bs4.element.Tag):
#             body_2.append(i.text.strip())
#     for i in range(0, len(body_2)):
#         if (i % 2) == 0:
#             information_body.append(
#                 [body_2[i], body_2[i+1]])
#     # packagin the athetics information section of athletics
#     information_obj = {
#         "header": header,
#         "body": information_body
#     }
#     print(information_obj)
#     print("_______")
# !!!!

# print(header)
# information_body = []
# body = section.find("dl", {"class": "profile-overview"})
# body_2 = []
# for i in body:
# print(i)
# if (type(i) == bs4.element.Tag):
# body_2.append(i.text.strip())
# for i in range(0, len(body_2)):
#     if (i % 2) == 0:
#         information_body.append(
#             [body_2[i], body_2[i+1]])
# # packagin the athetics information section of athletics
# information_obj = {
#     "header": header,
#     "body": information_body
# }
# print(information_obj)
# except:
#     print('\n no h6')
# print(section)
# print("_________")

# # !!!!!!!!!
# athletics_information = athletics_section.find(
#     'h6', {"class": "m-section-title"})
# athletics_information_header = athletics_information.text
# # !!!!!!!!!
# athletics_information_body = []
# athletics_body = athletics_section.find(
#     "dl", {"class": "profile-overview"})
# athletics_body_2 = []
# for i in athletics_body:
#     if (type(i) == bs4.element.Tag):
#         athletics_body_2.append(i.text.strip())
# for i in range(0, len(athletics_body_2)):
#     if (i % 2) == 0:
#         athletics_information_body.append(
#             [athletics_body_2[i], athletics_body_2[i+1]])
# # packagin the athetics information section of athletics
# athletics_information_obj = {
#     "header": athletics_information_header,
#     "body": athletics_information_body
# }
# # !!!!!!!
# college_name = soup.find('span', {"itemprop": "name"}).text
# # !!!!!!!
# college_street_adress = soup.find('span', {"itemprop": "streetAddress"}).text
# # !!!!!!!
# college_adress_locality = soup.find(
#     'span', {"itemprop": "addressLocality"}).text
# # !!!!!!!
# college_telephone = soup.find(
#     'span', {"itemprop": "telephone"}).text
# # !!!!!!!
# college_official_website = soup.find("ul", {"itemprop": "address"})
# college_official_website = college_official_website.find('a').text
# # !!!!!!!
# profile_overview = soup.find('dl', {'class': "profile-overview"})
# over_view_elems = []
# for overview in profile_overview:
#     if (type(overview) == bs4.element.Tag):
#         over_view_elems.append(overview.text)
# over_view_len = len(over_view_elems)
# new_over_view_elems = []
# for i in range(0, over_view_len):
#     listed = list(over_view_elems[i])
#     new_string = []
#     skip = False
#     for letter in listed:
#         if (skip == True):
#             # print('skipping')
#             skip = False
#         else:
#             if (letter == '\\'):
#                 skip = True
#                 # print('no')
#             else:
#                 new_string.append(letter)
#     new_over_view_elems.append(''.join(new_string))
# cleaned_over_view = []
# for i in new_over_view_elems:
#     cleaned_over_view.append(" ".join(i.split()))
# college_over_view = []
# for i in range(0, len(cleaned_over_view)):
#     if ((i % 2) == 0):
#         college_over_view.append(
#             [cleaned_over_view[i], cleaned_over_view[i+1]])
# # !!!!!!!
# print(college_over_view)

#     over_view_elems.append(overview)
# for elem in over_view_elems:
#         print(elem.text.strip())
#         print("______")

# def download_college_data(college, status_key):
# print('downloading', status_key, "for", college['name'])
# result = requests.get(state_url)
# THEOG # result = requests.get(college['link'])
# content = result.content
# print(content)
# 1.download the data
# if (status_key == "general_info"):

# 2.write to master
# 3.update stage_3.json
# if (status_key == "athletics_section")
# if (status_key == "admissions_section")
# if (status_key == "environment_section")
# if (status_key == "financial_section")

# def download():
#     f = open('stage_3.json', 'r')
#     f_read_map = f.read()
#     f_loaded_map = json.loads(f_read_map)
#     for college in f_loaded_map:
#         download_stats = college["isDownloaded"]
#         for status_key in download_stats:
#             if (download_stats[status_key] == False):
#                 download_college_data(college, status_key)
#         print('____________')
# pprint(f_loaded_map[0])

# download()
# try:
#     f = open("master.json", 'r')
#     f_read = f.read()
#     f_loaded_master = json.loads(f_read)
#     list_of_all_colleges = []
#     state_len = len(f_loaded_master)
#     state_count = 0
#     college_count = 0
#     for state in f_loaded_master:
#         if (state['hasLeague'] == True):
#             state_count = state_count + 1
#             state_prog = state_count / (state_len)
#             list_of_col = state['data']["list_of_colleges"]
#             list_of_col_len = len(list_of_col)
#             for college in list_of_col:
#                 college_count = college_count + 1
#                 college_prog = college_count / list_of_col_len
#                 college_map_obj = {
#                     "id": college_count,
#                     "state": state['name'],
#                     "name": college["name"],
#                     "link": college['href'],
#                     "isDownloaded": {
#                         "general_info": False,
#                         "athletics_section": False,
#                         "admissions_section": False,
#                         "environment_section": False,
#                         "financial_section": False
#                     }
#                 }
#                 print(college_prog / state_prog)
#                 list_of_all_colleges.append(college_map_obj)
#     # save the map
#     try:
#         print('storing the map for list_of_all_colleges')
#         f = open("stage_3.json", "a")
#         f.write(json.dumps(list_of_all_colleges))
#     except:
#         print('failed to create the map for list_of_all_colleges')
# except:
#     print('unable to create list of all colleges')

# for college in list_of_all_colleges:
#     pprint(college)
#     print('__________________')
#     print('__________________')

# result = requests.get(state_url)
# content = result.content
# soup = BeautifulSoup(content, 'lxml')
# # FOR SCHOOLS_OFFERING
# offerings = soup.find(id="schools_offering")
# # get title
# title = offerings.find("div").attrs['title']
# # get table and data
# table_data = []
# table_body = offerings.find_all("tr")
# for data in table_body:
#     data = data.text.strip().split('\n')
#     table_data.append(data)
# offerings_obj = {
#     "title": title,
#     "table_data": table_data
# }
# # print(obj)
# # +++++++
# scholarships = soup.find(id="scholarship_opportunities")
# title = scholarships.find("div").attrs['title']
# table_data = []
# table_body = scholarships.find_all("tr")
# for data in table_body:
#     data = data.text.strip().split('\n')
#     table_data.append(data)
# scholarships_obj = {
#     "title": title,
#     "table_data": table_data
# }
# # print(scholarships_obj)
# # +++++++
# athlete_participation = soup.find(id="student_athlete_participation")
# title = athlete_participation.find("div").attrs['title']
# table_data = []
# table_body = athlete_participation.find_all("tr")
# for data in table_body:
#     data = data.text.strip().split('\n')
#     table_data.append(data)
# athlete_participation_obj = {
#     "title": title,
#     "table_data": table_data
# }
# # print(athlete_participation_obj)
# state_general_stats = {
#     "offerings": offerings_obj,
#     "scholarships": scholarships_obj,
#     "participation": athlete_participation_obj
# }

# pprint(state_general_stats)
# driver.get(state_url)

# state_result = requests.get(state_url)
# state_soup = BeautifulSoup(state_result.content, 'lxml')
# stat_list = state_soup.find_all(
#     'div', id="schools_offering")
# state_general_stat = []
# for stat in stat_list:
#     str_obj = {}
#     str_array = stat.text.strip().split(":")
#     str_obj[str_array[0].strip()] = str_array[1].strip()
#     state_general_stat.append(str_obj)
# college_obj['general_stat'] = college_stats

# tables = schoolsOffering.find_all("tr")
# print(tables)
# print(stat_list)

# for stat in stat_list:
#     str_obj = {}
#     str_array = stat.text.strip().split(":")
#     str_obj[str_array[0].strip()] = str_array[1].strip()
#     college_stats.append(str_obj)
# college_obj['general_stat'] = college_stats

# _src = myElem.get_attribute('innerHTML')
# soup = BeautifulSoup(_src, 'lxml')
# driver.quit()

# except expression as identifier:
# pass
# finally:
# pass
# print(schoolsOffering.prettify())
#  !!!!!!!
# stat_list = college_data_soup.find_all(
#     'div', {"class": "college_map_stats"})
# college_stats = []
# for stat in stat_list:
#     str_obj = {}
#     str_array = stat.text.strip().split(":")
#     str_obj[str_array[0].strip()] = str_array[1].strip()
#     college_stats.append(str_obj)
# college_obj['general_stat'] = college_stats

# _src = myElem.get_attribute('innerHTML')
# soup = BeautifulSoup(_src, 'lxml')
# driver.quit()


# print('________________________________________')
# print('________________________________________')
# f.close()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# f = open('test.html','a')
# table = soup.find(id="schools_offering")
# print(soup.find(id="stats_container"))
# first_table = (soup.find('table', {"class": "sport_stats"}))
# print(first_table)


# links = soup.find_all('a')
# links = links[6:57]


# state_list = []
# for link in links:
#     obj = {
#         "link": link.attrs['href'],
#         "name": link.text
#     }
#     state_list.append(obj)

# f = open('1_states.json', 'w')
# f.write(json.dumps(state_list))
# f.close()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# try:
# myElem = WebDriverWait(driver, delay).until(
# EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[3]")))
# print("Page is ready!")
# except TimeoutException:
# print("Loading took too much time!")
# print('________________________________________')


# _src = myElem.get_attribute('innerHTML')
# soup = BeautifulSoup(_src, 'lxml')
# school_offerings = soup.find_all('div')
# school_offerings_range = len(school_offerings)

# list_of_colleges = []
# f = open("modal.txt", 'r')
# list_of = f.read().split("+++")
# for college_data in list_of:
#     college_obj = {}
#     college_data_soup = BeautifulSoup(college_data, 'lxml')

#  !!!!!!!
# college_obj["name"] = college_data_soup.find("a").text

#  !!!!!!!
# stat_list = college_data_soup.find_all(
#     'div', {"class": "college_map_stats"})
# college_stats = []
# for stat in stat_list:
#     str_obj = {}
#     str_array = stat.text.strip().split(":")
#     str_obj[str_array[0].strip()] = str_array[1].strip()
#     college_stats.append(str_obj)
# college_obj['general_stat'] = college_stats

#  !!!!!!!!
# print(college_data_soup.prettify())
# print('________________________________________')
# when done building the obj, pack it up
# list_of_colleges.append(college_obj)
# print(list_of_colleges)


# for i in range(1, school_offerings_range):
# print('________________________________________')
# elem = driver.find_element_by_xpath(
# f'/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[3]/div[{i}]')
# driver.execute_script("arguments[0].click();", elem)
# try:
# data_console = WebDriverWait(driver, delay).until(
# EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/div/div")))
# print("Page is ready!")
# except TimeoutException:
# print("Loading took too much time!")
# college_data = data_console.get_attribute('innerHTML')

# f.write(f'{str(college_data)}+++')

# print('________________________________________')
# print('________________________________________')

# ----- -> >> >


# college_obj = {}
# college_data_soup = BeautifulSoup(college_data, 'lxml')
# # print(college_data_soup.prettify())

#  !!!!!!!
# college_obj["name"] = college_data_soup.find("a").text
#  !!!!!!!
# college_obj["adress"]  = college_data_soup.find('div',{"class":"college_map_address"}).text
#  !!!!!!!
# college_obj["title"]  = college_data_soup.find("a").attrs["title"]
#  !!!!!!!
# href = college_data_soup.find("a").attrs["href"]
# college_obj['href'] = f'{base_url}{href}'
#  !!!!!!!
# college_obj['image'] = college_data_soup.find("img").attrs["src"]
#  !!!!!!!
# stat_list = college_data_soup.find_all(
#     'div', {"class": "college_map_stats"})
# college_stats = []
# for stat in stat_list:
#     str_obj = {}
#     str_array = stat.text.strip().split(":")
#     str_obj[str_array[0].strip()] = str_array[1].strip()
#     college_stats.append(str_obj)
# college_obj['general_stat'] = college_stats

# when done building the obj, pack it up
# list_of_colleges.append(college_obj)
# write the list into master file on each itteration
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# f = open('1_states.json', 'r')
# content = f.read()
# loaded_content = json.loads(content)
# f.close()

# for states in loaded_content:
#     state_result = requests.get(states['link'])
#     state_soup = BeautifulSoup(state_result.content, 'lxml')
#     state_map_canvas = state_soup.find_all(id="map_canvas")
#     if (len(state_map_canvas) == True):
#         states.update({"hasLeague": True})
#     else:
#         states.update({"hasLeague": False})


# x = open('2_state.json', 'w')
# data = json.dumps(loaded_content)
# x.write(data)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
