from bs4 import BeautifulSoup
import re
import time
import os
from urllib.request import urlopen


HTML_FILES_DIRECTORY = r'C:\Users\Ravi\PycharmProjects\IRassignment\Results\dfs\Raw HTML files'


def collect_sites(first_link):
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
        url = "https://en.wikipedia.org%s" % site
        if '#' in site:
            url = url.split('#')[0]
        if (url.find("en") > 0) and ((url in fresh_sites) == False) and ((":" in site) == False):
            fresh_sites.insert(len(fresh_sites), url)
        i = i + 1
    return fresh_sites


def finder(first, present_depth, limit_of_urls, relevant_links):
    limit_of_depth = 6
    if present_depth <= limit_of_depth and len(relevant_links) < limit_of_urls and (first not in relevant_links):
        relevant_links.append(first)
        main_crawler = collect_sites(first)
        filter(lambda x: len(relevant_links) < limit_of_urls and limit_of_depth > present_depth and (
                    x not in relevant_links), main_crawler)
        pos = 0
        while pos < len(main_crawler):
            fresh_urls_collector = finder(main_crawler[pos], present_depth + 1, limit_of_urls, relevant_links)
            i = 0
            while i < len(fresh_urls_collector):
                if fresh_urls_collector[i] not in relevant_links:
                    relevant_links.append(fresh_urls_collector[i])
                i = i + 1
            pos = pos + 1
        time.sleep(1)
    return relevant_links


URL_DIRECTORY = r'C:\Users\Ravi\PycharmProjects\IRassignment\Results\dfs'

if not os.path.exists(HTML_FILES_DIRECTORY):
    os.makedirs(HTML_FILES_DIRECTORY)
fileList = os.listdir(HTML_FILES_DIRECTORY)
if fileList is not []:
    list(map(lambda f: os.remove(HTML_FILES_DIRECTORY + '/' + f), fileList))
present_depth = 1
limit_of_urls = 1000
first = "https://en.wikipedia.org/wiki/Solar_eclipse"
print("Please wait")
relevant_links = list()
url_list = finder(first, present_depth, limit_of_urls, relevant_links)
open_text = open(URL_DIRECTORY + "\List_of_links.txt", 'w')
index = 0
while index < (len(url_list)):
    open_text.write(str(index + 1))
    open_text.write(") ")
    open_text.write(url_list[index])
    open_text.write("\n")
    index = index + 1
print("List_of_links.txt and Raw HTML files have been created")
