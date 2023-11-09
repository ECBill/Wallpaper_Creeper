import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import pickle
import undetected_chromedriver as uc
import glob

path = './result/'

def fetch_pic_url(url):
    href = None
    try:
        browser = uc.Chrome()
    except:
        try:
            browser = uc.Chrome()
        except:
            print(url)
            return None
    try:
        browser.get(url)
    except:
        try:
            browser.get(url)
        except Exception as e:
            print(e)
            print(url)
            return None
    try:
        html_data = browser.page_source
        soup = BeautifulSoup(html_data, "html.parser")
        li_tag = soup.find('li', {'id': 'post-info-size'})
        a_tag = li_tag.find('a')
        href = a_tag['href']
        browser.close()
    except Exception as e:
        print(e)
        print('未找到图片:' + url)
        browser.close()

    if not href:
        return None
    return href


def down_from_url(href):
    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(href)
        with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
            f.write(response.content)
    except:
        try:
            session = requests.Session()
            session.trust_env = False
            response = session.get(href)
            with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)
            return 0
    return 1

def trans_pic_url():
    error = list()
    target = list()
    with open('all_urls.pkl', 'rb') as f:
        data = pickle.load(f)
        count = len(data)
        pic_num = 0
        for p_url in data:
            pic_url = fetch_pic_url(p_url)
            if not pic_url:
                pic_url = fetch_pic_url(p_url)
                if not pic_url:
                    error.append(p_url)
                else:
                    target.append(pic_url)
            pic_num+=1
            print("第"+str(pic_num)+"张图片处理完成,共有"+str(count)+"张")
    f.close()

    with open('trans_urls.pkl', 'wb') as file:
        pickle.dump(target, file)
    with open('error_urls.pkl', 'wb') as file:
        pickle.dump(error, file)


def down_pic():
    error = list()
    with open('trans_urls.pkl', 'rb') as f:
        data = pickle.load(f)
        count = len(data)
        pic_num = 1
        for p_url in data:
            result = down_from_url(p_url)
            if not result:
                result = down_from_url(p_url)
                if not result:
                    error.append(pic_num)
            print("第" + str(pic_num) + "张图片处理完成,共有" + str(count) + "张")
            pic_num += 1
    f.close()
    with open('down_error_urls.pkl', 'wb') as file:
        pickle.dump(error, file)
    file.close()

down_pic()