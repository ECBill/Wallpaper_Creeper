import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import pickle
import undetected_chromedriver as uc
import glob

path = './result/'

def down_pic_url(url):
    href = ''
    try:
        browser = uc.Chrome()
        browser.get(url)
        html_data = browser.page_source
        soup = BeautifulSoup(html_data, "html.parser")
        # links = soup.find_all('li', id_='post-info-size')
        li_tag = soup.find('li', {'id': 'post-info-size'})
        a_tag = li_tag.find('a')
        href = a_tag['href']
        browser.close()
    except:
        try:
            browser = uc.Chrome()
            browser.get(url)
            html_data = browser.page_source
            soup = BeautifulSoup(html_data, "html.parser")
            # links = soup.find_all('li', id_='post-info-size')
            li_tag = soup.find('li', {'id': 'post-info-size'})
            a_tag = li_tag.find('a')
            href = a_tag['href']
            browser.close()
        except:
            print(url)
    if not href:
        return
    try:
        response = requests.get(href)
        with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
            f.write(response.content)
    except:
        try:
            response = requests.get(href)
            with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
                f.write(response.content)
        except:
            response = requests.get(href)
            with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
                f.write(response.content)
    return

def read_from_pkl():
    # 获取当前目录下所有的.pkl文件
    file_pattern = os.path.join(os.path.dirname(__file__), '*.pkl')
    pkl_files = glob.glob(file_pattern)

    # 遍历.pkl文件并读取它们
    for pkl_file in pkl_files:
        print("正在载入："+pkl_file)
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
            for urls in data:
                for p_url in urls:
                    down_pic_url(p_url)
        print(pkl_file+'下载完成')
        os.remove(pkl_file)


read_from_pkl()