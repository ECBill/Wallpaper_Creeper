import os
import re
import time

import requests as requests
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def get_imgs(kcode):
    opt = uc.ChromeOptions()
    opt.add_argument(argument="headless")
    browser = uc.Chrome(options=opt)
    url = 'https://nhentai.to/g/'+kcode
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    img_list = list()
    a = soup.find_all('a', class_='gallerythumb')
    browser.close()
    browser.quit()
    for a_tag in a:
        # 找到每个a标签下的img标签
        img_tag = a_tag.find('img')
        # 获取img标签内的data-src值
        data_src = img_tag.get('data-src')
        pattern = r'(\d+)t'
        replacement = r'\1'
        data_src = re.sub(pattern, replacement, data_src)
        img_list.append(data_src)

    l = len(img_list)
    path = './result/'
    j = 1
    for src in img_list:
        response = requests.get(src)
        with open(os.path.join(path, os.path.basename(src)), 'wb') as f:
            f.write(response.content)
        print('one page finished! '+str(j)+'/'+str(l))
        j+=1
    print('All pages finished.')


if __name__ == '__main__':
    get_imgs('406591')