import uiautomation as auto
import time
import sys
from urllib.parse import urlparse
import math
import datetime
import json
import os.path

# Variables for url tracking
old_link = ""
new_link = ""


urls_dict = {}  # Dictionary for url and time tracking
total_time = 0  # Variable to track time spent in each url before changing


# URL Parser
# gets the basic detail of the website (google.com for example)
def parse_url(url):
    o = urlparse(new_link)
    url_split = o.path.split("/", 1)
    return url_split[0]


# Json dumper
def json_dumper(data, file):
    with open(file, 'w') as jsonFile:
        json.dump(data, jsonFile)


# Json loader
def json_loader(file):
    with open(file, 'r') as jsonFile:
        return json.load(jsonFile)

# Obtained from:
# https://stackoverflow.com/questions/52675506/get-chrome-tab-url-in-python
def get_browser_tab_url(browser: str):
    """
    Get browser tab url, browser must already open
    :param browser: Support 'Edge' 'Google Chrome' and other Chromium engine browsers
    :return: Current tab url
    """
    if browser.lower() == 'edge':
        addr_bar = auto.EditControl(AutomationId='addressEditBox')
    else:
        win = auto.PaneControl(
            Depth=1, ClassName='Chrome_WidgetWin_1', SubName=browser)
        temp = win.PaneControl(Depth=1, Name=browser).GetChildren()[
            1].GetChildren()[0]
        for bar in temp.GetChildren():
            last = bar.GetLastChildControl()
            if last and last.Name != '':
                break
        addr_bar = bar.GroupControl(Depth=1, Name='').EditControl()
    url = addr_bar.GetValuePattern().Value
    return url


if __name__ == "__main__":
    while True:
        try:
            start_time = time.time()
            new_link = get_browser_tab_url('Google Chrome')

            # If the url is the same, keep adding the total time and update the dictionary
            if new_link == old_link and new_link != "":
                total_time = total_time + (time.time() - start_time)
                url = parse_url(new_link)
                if url in urls_dict:
                    urls_dict[url] += total_time
                    total_time = 0
                elif url not in urls_dict:
                    urls_dict[url] = total_time

            # If the url changes, update old_link and reset time
            elif new_link != old_link and new_link != "":
                old_link = new_link
                total_time = 0
                total_time = total_time + (time.time() - start_time)
                url = parse_url(new_link)
                if url in urls_dict:
                    urls_dict[url] += total_time
                elif url not in urls_dict:
                    urls_dict[url] = total_time

        except (KeyboardInterrupt, SystemExit):
            # If file doesn't exist, just create new one and insert data
            if not os.path.isfile('data/urls_time.json'):
                json_dumper(urls_dict, 'data/urls_time.json')

            # If the file exists, need to import old data, update the data, then rewrite file content
            if os.path.isfile('data/urls_time.json'):
                data = json_loader('data/urls_time.json')

                for url in urls_dict:
                    if url in data:
                        data[url] = data[url] + urls_dict[url]
                    else:
                        data[url] = urls_dict[url]

                json_dumper(data, 'data/urls_time.json')

            sys.exit()
