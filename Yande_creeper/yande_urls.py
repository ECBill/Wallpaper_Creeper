import os
import pickle
from bs4 import BeautifulSoup
import requests as requests

web_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://yande.re/',
    'Connection': 'keep-alive',
    };

url1 = 'https://yande.re/post?page='
url2 = '&tags=zootopia'
#masou_gakuen_hxh
page=1
urls = list()
while True:
    url_n = url1+str(page)+url2
    req = requests.get(url=url_n, headers=web_header);
    req.encoding = 'utf-8'
    html_data = req.text
    soup = BeautifulSoup(html_data, "html.parser")
    links = list()
    linkss = soup.find_all('a', class_='directlink largeimg')
    links += linkss
    linkss = soup.find_all('a', class_='directlink smallimg')
    links += linkss
    if links == []:
        break
    for link in links:
        urls.append(link.get('href'))
    page+=1
links = list()
l = len(urls)
j=1
path = './result/'
for url in urls:
    # if j<1033:
    #     j+=1
    #     continue
    response = requests.get(url,headers=web_header)
    with open(os.path.join(path, str(j)+os.path.basename(url)[-4:]), 'wb') as f:
        f.write(response.content)
    print('one page finished! ' + str(j) + '/' + str(l))
    j += 1
print('All pages finished.')
