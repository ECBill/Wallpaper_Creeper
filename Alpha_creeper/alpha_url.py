from selenium import webdriver
from selenium.webdriver.common.by import By

def get_url(key_word):
    # 创建浏览器对象
    option = webdriver.ChromeOptions()
    #option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
    # 打开网页
    browser.get('https://wall.alphacoders.com/')

    # 找到搜索框并输入关键词
    input_box = browser.find_element(By.CSS_SELECTOR, 'input.search-bar.form-control.input-lg')
    input_box.send_keys(key_word)

    # 找到搜索按钮并点击
    search_button = browser.find_element(By.CSS_SELECTOR, '[id="search_zone_index"] > .input-group-btn')
    search_button.click()
    # 获取搜索结果页面的网址
    result_url = browser.current_url
    browser.get(result_url)
    result_url = browser.current_url
    res = result_url+'&quickload=1200+&page='
    return res