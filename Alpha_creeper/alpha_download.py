from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

def download(url):
    option = webdriver.ChromeOptions()
    # option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
    i = 1
    srcs = list()
    while True:
        browser.get(url + str(i))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        link_1 = soup.find_all('img', class_='img-responsive big-thumb thumb-desktop')
        link_2 = soup.find_all('img', class_='img-responsive thumb-desktop')
        links = link_1+link_2
        #print(links)
        if links == []:
            break
        for img_tag in links:
            src = img_tag.get('src')
            srcs.append(src)
        i += 1
    l=len(srcs)
    print(l)
    path = './result/'
    j=1
    for src in srcs:
        response = requests.get(src)
        with open(os.path.join(path, os.path.basename(src)), 'wb') as f:
            f.write(response.content)
        print('one page finished! '+str(j)+'/'+str(l))
        j+=1
    print('All pages finished.')
