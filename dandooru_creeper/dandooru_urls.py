import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import pickle
import undetected_chromedriver as uc


def get_index_url(url):
    browser = uc.Chrome()
    browser.get(url)
    html_data = browser.page_source
    soup = BeautifulSoup(html_data, "html.parser")
    links = soup.find_all('a', class_='post-preview-link')
    browser.close()
    urls = list()
    for link in links:
        urls.append('https://danbooru.donmai.us/'+link.get('href'))
    return urls

def go_through_pages(url1,url2):
    page = 261
    index_url = list()
    while True:
        url_n = url1 + str(page) + url2
        try:
            links = get_index_url(url_n)
        except:
            time.sleep(5)
            try:
                links = get_index_url(url_n)
            except:
                print(str(page)+"wrong!")
        if links == []:
            for i in range(3):
                try:
                    links = get_index_url(url_n)
                except:
                    time.sleep(5)
                    links = get_index_url(url_n)
                if links != []:
                    break
            if links == []:
                break
        index_url.append(links)
        print(str(page)+' over')
        if page%10 == 0:
            with open('index_url'+str(page/10)+'.pkl', 'wb') as file:
                pickle.dump(index_url, file)
            index_url = list()
        page += 1
    with open('index_url' + str(page/10) + '.pkl', 'wb') as file:
        pickle.dump(index_url, file)


origin_url1 = 'https://danbooru.donmai.us/posts?page='
origin_url2 = '&tags=xenoblade_chronicles_2+'
go_through_pages(origin_url1,origin_url2)