import urllib.robotparser
import gzip
import time
import requests
from bs4 import BeautifulSoup

filename = "urllist.txt"

rp = urllib.robotparser.RobotFileParser()
rp.set_url("http://newspicks.com/robots.txt")
rp.read()

for map in rp.site_maps() :
    time.sleep(1)
    re = requests.get(map)
    soup = BeautifulSoup(re.content, "xml")
    for loc in soup.find_all('loc') :
        url = loc.text
        time.sleep(1)
        print(url)
        loc_re = requests.get(url)
        if url[-2:] == 'gz' :
            loc_re_content = gzip.decompress(loc_re.content)
        else :
            loc_re_content = loc_re.content
        loc_re_soup = BeautifulSoup(loc_re_content, "xml")
        for locloc in loc_re_soup.find_all('loc') :
            print('- ', locloc.text)
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(locloc.text + '\n')