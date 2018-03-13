from bs4 import BeautifulSoup
import time
import os
from urllib.request import urlopen
import re

print("Processing.....")

HTML_FILES_DIRECTORY = r'C:\Users\Ravi\PycharmProjects\IRassignment\Results\key\Raw HTML files'

def collect_sites(first_link, keywords):
    source = BeautifulSoup(urlopen(first_link), "html.parser")
    sites = source.find("div", {"id": "mw-content-text"}).find_all('a', href=re.compile('^/wiki/'))
    former, topic_name = first_link.split("wikipedia.org/wiki/")
    rawfile = (topic_name + ".txt").replace("/", "_")
    open_html = open(HTML_FILES_DIRECTORY + "\\" + rawfile, 'w', encoding="UTF-8")
    open_html.write(first_link + "\n" + source.prettify())
    fresh_sites = list()
    i = 0
    while i < len(sites):
        site = sites[i].get('href')
        url = "https://en.wikipedia.org%s"%site
        if '#' in site:
            url = url.split('#')[0]
        anchor = sites[i].text
        for key in keywords:
            url_upper = int(url.upper().find(key))
            url_lower = int(url.lower().find(key))
            anchor_upper = int(anchor.upper().find(key))
            anchor_lower = int(anchor.lower().find(key))
            if ((url.find("en") > 0) and ((url in fresh_sites) == False) and ((":" in site) == False) and (
                    (url_upper >= 0) or (url_lower >= 0) or (anchor_upper >= 0) or (anchor_lower >= 0))):
                fresh_sites.insert(len(fresh_sites), url)
        i = i + 1
    return fresh_sites


def finder(first, limit_of_depth, limit_of_urls, keywords):
    main_crawler = [first]
    relevant_links = []
    temp_urls = []
    depth_level = 1
    while depth_level <= limit_of_depth and len(relevant_links) < limit_of_urls:
        if bool(main_crawler):
            first_link = main_crawler[0]
            del main_crawler[0]
            if first_link in relevant_links:
                continue
            else:
                fresh_urls_collector = collect_sites(first_link, keywords)
                if not bool(fresh_urls_collector):
                    continue
                else:
                    index = 0
                    while index < len(fresh_urls_collector):
                        if fresh_urls_collector[index] not in temp_urls:
                            temp_urls.insert(len(temp_urls), fresh_urls_collector[index])
                        index = index + 1
                    relevant_links.insert(len(relevant_links), first_link)
                    time.sleep(1)
            if bool(main_crawler):
                continue
            else:
                main_crawler = temp_urls
                for i in temp_urls:
                    del i
                depth_level = depth_level + 1
                print(depth_level)
    return relevant_links


URL_DIRECTORY = r'C:\Users\Ravi\PycharmProjects\IRassignment\Results\key'

if not os.path.exists(HTML_FILES_DIRECTORY):
    os.makedirs(HTML_FILES_DIRECTORY)
fileList = os.listdir(HTML_FILES_DIRECTORY)
if fileList is not []:
    list(map(lambda f: os.remove(HTML_FILES_DIRECTORY + '/' + f), fileList))
limit_of_depth = 6
limit_of_urls = 1000
keywords = ["lunar", "moon"]
first = "https://en.wikipedia.org/wiki/Solar_eclipse"
print("Please wait")
url_list = finder(first, limit_of_depth, limit_of_urls, keywords)
open_text = open(URL_DIRECTORY + "\List_of_links.txt", 'w')
index = 0
while index < (len(url_list)):
    open_text.write(str(index + 1))
    open_text.write(") ")
    open_text.write(url_list[index])
    open_text.write("\n")
    index = index + 1
print("List_of_links.txt and Raw HTML files have been created")
