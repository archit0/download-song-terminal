#!/usr/bin/python
import sys
from bs4 import BeautifulSoup
import requests
import re
from urlparse import  urljoin
import json
from subprocess import call

if(len(sys.argv) == 1):
    print 'Sample Query: python {} "{}" '.format(sys.argv[0],"QUERY_STRING")
    sys.exit(0)

def get_source_code(url):
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}).content
    return BeautifulSoup(html,"html.parser")

def extract(regex, content, group_num):
    result = []
    for match in re.finditer(r'{}'.format(regex), str(content)):
        result.append(match.group(group_num))
    return result

def download(url):
    call(['wget',url])

query = sys.argv[1]+" mp3 download"
search_result = get_source_code("https://www.google.com/search?q=" + query)
search_result_url = extract('<cite.*?>(.*?)<\/cite><div class="action-menu', search_result, 1)

output = []
for target_url in  search_result_url:
    if not target_url.lower().startswith("http") and not target_url.lower().startswith("https"):
        target_url = "http://"+target_url
    try:
        for url in get_source_code(target_url).find_all('a'):
                abs_url = urljoin(target_url,url.get('href'))
                if(abs_url.lower().endswith(".mp3")):
                    output.append(abs_url)
    except Exception,e:
        print e

for index,value in enumerate(output):
    print "[{}]: {}".format(index, value)

to_download_index = int(raw_input("Enter index to download: "))
download(output[to_download_index])
