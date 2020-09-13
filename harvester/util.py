import json
from pprint import pprint
import time

f = open('college_list.json', "r")
college_list = json.loads(f.read())
f.close()

for college in college_list:
    print(college['isDownloaded'])
#     college['isDownloaded'].update({
#         "environment_section": False
#     })

# f = open('college_list.json', "w")
# f.write(json.dumps(college_list))
# f.close()
