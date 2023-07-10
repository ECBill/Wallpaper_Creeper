import time

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import undetected_chromedriver as uc


def download(url):
    opt = uc.ChromeOptions()
    #opt.add_argument(argument="headless")
    browser = uc.Chrome(options=opt)
    i = 0
    srcs = list()
    while True:
        i+=1
        browser.get(url + str(i))
        try:
            html = browser.page_source
        except:
            break
        soup = BeautifulSoup(html, 'lxml')
        link_1 = soup.find_all('img', class_='img-responsive big-thumb thumb-desktop')
        link_2 = soup.find_all('img', class_='img-responsive thumb-desktop')
        link_3 = soup.find_all('img', class_='img-responsive big-thumb')
        links = link_1+link_2+link_3
        #print(links)
        if links == []:
            time.sleep(10)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            link_1 = soup.find_all('img', class_='img-responsive big-thumb thumb-desktop')
            link_2 = soup.find_all('img', class_='img-responsive thumb-desktop')
            link_3 = soup.find_all('img', class_='img-responsive big-thumb')
            links = link_1 + link_2 + link_3
            if links == []:
                break
        for img_tag in links:
            src = img_tag.get('src')
            srcs.append(src)
    l=len(srcs)
    print(l)
    path = './result/'
    j=1
    for src in srcs:
        src = src.replace("thumbbig-","")
        response = requests.get(src)
        with open(os.path.join(path, os.path.basename(src)), 'wb') as f:
            f.write(response.content)
        print('one page finished! '+str(j)+'/'+str(l))
        j+=1
    print('All pages finished.')
