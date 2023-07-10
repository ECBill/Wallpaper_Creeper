import time
import requests as requests
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def get_url(key_word):
    opt = uc.ChromeOptions()
    opt.add_argument(argument="headless")
    browser = uc.Chrome(options=opt)
    url = 'https://wall.alphacoders.com/search.php?search=' + key_word
    browser.get(url)
    browser.refresh()
    result_url = browser.current_url
    browser.close()
    res = result_url+'&quickload=230+&page='
    browser.quit()
    return res

def get_url_byapi(key_word):

    url = 'https://wall.alphacoders.com/search.php?search='+key_word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': 'https://wall.alphacoders.com/',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.76786876.1681444451; _ga_HL65XQTV30=GS1.1.1681786244.2.0.1681786253.0.0.0; wa_session=2j1furk2ekgs498303smt6jbmc; __gads=ID=df94771fa916475a-228c63a731df0040:T=1681444451:RT=1687761225:S=ALNI_MYDNaolN5v35yqmxR51Ff4kjeDEPw; __gpi=UID=00000bf45c3d65d8:T=1681444451:RT=1687761225:S=ALNI_MZBSBpKadxcoFlO2pntjQtZKvYezA; __cf_bm=W9vNFw_KR8k2aj06_bIDbLBjuzvHvkqASQkp7hYAH78-1687761225-0-AePw1GzO9JiQ+Q/zCuRlBEU/14pOjcMh6zwR7QBs+ns61m9pr7iRFyg0T+D7ryePSpwqZB3b24WTbQHl1jifA/RAQdvtbquAISyzBAJiccNG; cto_bundle=njAYBl8zZ2tXWTNrbzJGaG1DT1pEM1hqV2NEODU3b2Y2WDU0Y1JKQUIzM1VwVFhOT0ZYUGxQVnNSdkhRYTBLWFlyb0FZRWFEbFhMOHpVcE9qVGdHYzd6bnB6ZEIlMkJSVThZVHhBQ3Y3NlpHOGhBOWJ2JTJGSVklMkZjeXFQcmNLQTg1YUwzaG5seHRYTGJib2x2enpoY3ZKJTJCaTNvaUNFZyUzRCUzRA',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'Sec-Ch-Ua-Mobile' : '?0',
        'Sec-Ch-Ua-Platform' : '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests' : '1'
    }

    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    meta_tag = soup.find("meta", {"property": "og:url"})
    url = meta_tag["content"]
    res = url + '&quickload=230+&page='
    return res


def get_url_past(key_word):
    option = webdriver.ChromeOptions()
    option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    browser = webdriver.Chrome(options=option)
    # 打开网页
    browser.get('https://wall.alphacoders.com/')
    time.sleep(3)
    # 找到搜索框并输入关键词
    input_box = browser.find_element(By.CSS_SELECTOR, 'input.search-bar.form-control.input-lg')
    input_box.click()
    time.sleep(1.1)
    input_box.send_keys(key_word)

    # 找到搜索按钮并点击
    search_button = browser.find_element(By.CSS_SELECTOR, '[id="search_zone_index"] > .input-group-btn')
    time.sleep(1.2)
    search_button.click()
    browser.refresh()
    # 获取搜索结果页面的网址
    result_url = browser.current_url
    browser.get(result_url)
    time.sleep(2)
    result_url = browser.current_url
    res = result_url + '&quickload=230+&page='
    return res
