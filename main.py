import uiautomation as auto
import time
import sys
from urllib.parse import urlparse
import math
import datetime


# Parse the new url to get only the basic website info
def parse_url(url):
    o = urlparse(new_link)
    url_split = o.path.split("/", 1)
    return url_split[0]


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


old_link = ""
new_link = ""

urls_dict = {}
total_time = 0

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

    except KeyboardInterrupt:
        # TODO: export dictionary information to json file
        print("----------")
        for url, time in urls_dict.items():
            print("Url:", url)
            print("Time spent:", str(datetime.timedelta(seconds=int(time))))
            print("----------")
        exit()
