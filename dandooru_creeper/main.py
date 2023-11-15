import glob
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pickle
import undetected_chromedriver as uc

path = './result/'


# 初始化uc
def initialize_browser():
    try:
        return uc.Chrome()
    except:
        print("Failed to initialize browser.")
        return None


# 取每个查询页的每个详情页链接
def get_index_url(browser, url):
    try:
        browser.get(url)
    except:
        try:
            browser.get(url)
        except:
            return 404
    html_data = browser.page_source
    soup = BeautifulSoup(html_data, "html.parser")
    links = soup.find_all('a', class_='post-preview-link')
    urls = list()
    for link in links:
        urls.append('https://danbooru.donmai.us/' + link.get('href'))
    return urls


# 取所有目标查询的详情页链接
def go_through_pages(key_word):
    url1 = 'https://danbooru.donmai.us/posts?page='
    url2 = '&tags=' + key_word
    page = 1
    index_url = list()
    browser = initialize_browser()
    if not browser:
        print("browser启动失败")
        return
    while True:
        url_n = url1 + str(page) + url2
        links = list()
        error = list()
        links = get_index_url(browser, url_n)
        if links == 404:
            time.sleep(5)
            links = get_index_url(browser, url_n)
            if links == 404:
                print(str(page) + "wrong!")
                error.append(page)
        if links == []:
            for i in range(3):
                try:
                    links = get_index_url(browser, url_n)
                except:
                    time.sleep(5)
                    links = get_index_url(browser, url_n)
                if links != []:
                    break
            if links == []:
                break
        index_url.extend(links)
        print(str(page) + ' over')
        page += 1
    browser.quit()
    with open('index_urls.pkl', 'wb') as file:
        pickle.dump(index_url, file)


# 取详情页里面图片的url
def fetch_pic_url(browser, url):
    href = None
    try:
        browser.get(url)
    except:
        try:
            browser.get(url)
        except:
            print(url)
            # browser.quit()
            return None
    try:
        html_data = browser.page_source
        soup = BeautifulSoup(html_data, "html.parser")
        li_tag = soup.find('li', {'id': 'post-info-size'})
        a_tag = li_tag.find('a')
        href = a_tag['href']
        # browser.quit()
    except:
        print('未找到图片:' + url)
        # browser.quit()

    if not href:
        return None
    return href


# 从url下载图片
def down_from_url(href):
    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(href, timeout=15)
        with open(os.path.join(path, os.path.basename(href)), 'wb') as f:
            f.write(response.content)
    except:
        print('图片下载失败:' + href)
        return href
    return None


# 把所有的详情链接转换成图片url
def trans_pic_url():
    error = list()
    target = list()
    browser = initialize_browser()
    if not browser:
        print("browser启动失败")
        return
    with open('index_urls.pkl', 'rb') as f:
        data = pickle.load(f)
        count = len(data)
    f.close()
    pic_num = 0
    page_num = 0
    for p_url in data:
        '''if pic_num<2399:
            pic_num+=1
            continue'''
        pic_url = fetch_pic_url(browser, p_url)
        if not pic_url:
            pic_url = fetch_pic_url(browser, p_url)
            if not pic_url:
                error.append(p_url)
            else:
                target.append(pic_url)
        else:
            target.append(pic_url)
        pic_num += 1
        page_num += 1
        print("第" + str(pic_num) + "张图片处理完成,共有" + str(count) + "张")
        '''if page_num >= 1000:
            with open('trans_' + str(page_num / 1000) + 'urls' + '.pkl', 'wb') as file:
                pickle.dump(target, file)
                target = list()
                page_num = 0'''

    with open('trans_urls.pkl', 'wb') as file:
        pickle.dump(target, file)
    with open('error_urls.pkl', 'wb') as file:
        pickle.dump(error, file)
    browser.quit()


def after_trans():
    browser = initialize_browser()
    if not browser:
        print("browser启动失败")
        return
    target = list()
    with open('error_urls.pkl', 'rb') as f:
        data = pickle.load(f)
        count = len(data)
    f.close()
    pic_num = 0
    for p_url in data:
        pic_url = fetch_pic_url(browser, p_url)
        if not pic_url:
            pic_url = fetch_pic_url(browser, p_url)
            if pic_url:
                target.append(pic_url)
        else:
            target.append(pic_url)
        pic_num += 1
        print("第" + str(pic_num) + "张错误处理完成,共有" + str(count) + "张")
    browser.quit()
    with open('trans_after_urls.pkl', 'wb') as file:
        pickle.dump(target, file)


# 把所有图片下载下来
def download():
    file_pattern = os.path.join(os.path.dirname(__file__), '*.pkl')
    pkl_files = glob.glob(file_pattern)
    error_list = list()
    # 遍历.pkl文件并读取它们
    x = 0
    for pkl_file in pkl_files:
        print("正在载入：" + pkl_file)
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
            count = len(data)
        f.close()
        now = 1
        for url in data:
            print("download:" + str(now) + '/' + str(count))
            dd = down_from_url(url)
            if dd:
                error_list.append(url)
            now += 1
        if error_list:
            with open(str(x) + 'error_downs.pkl', 'wb') as file:
                pickle.dump(error_list, file)
            error_list = list()
        print(pkl_file + '抽取完成')
        x += 1


key = 'amagami+'
#go_through_pages(key)
#trans_pic_url()
#after_trans()
download()
