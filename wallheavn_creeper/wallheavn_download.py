import os
import pickle
import time

from bs4 import BeautifulSoup
import requests as requests

web_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://wallhaven.cc/',
    'Connection': 'keep-alive',
    'Cookie': '_pk_id.1.01b8=99da255d3e3d2c03.1681870764.; _pk_ses.1.01b8=1; XSRF-TOKEN=eyJpdiI6InFYZjVNdTA0QW5QSTdhMnQrZE81NXc9PSIsInZhbHVlIjoiZ1daWFwvYVVid3hTOFY1TG0ySEZiN2dxa3RzTms2TEZyMUZzZW1mMURYNlVtYytpQTZKYWFrcFwvaXFDNVdObXNrIiwibWFjIjoiM2VkODZlNjljYTkzYTJjMDU2YTIyNjM5YmNlOWFhYmY5MzU3YzYyNjVhNjVhM2UyZGZlZmNmYTZjN2ZhZGVjNCJ9; wallhaven_session=eyJpdiI6Ilhoalc4ZnBiVmF5bzdcL1lXMHlEWFwvdz09IiwidmFsdWUiOiIrUkdLaHZaTHVIZStoMTJPb3JKcnMzeDlNd0ZaclEyQUFYYlFvcWtuZUNOSlQ0cEM5SVF5RzVISjExXC9pUkFIMyIsIm1hYyI6IjhhYzVkOGQwMGZhMWZhYmZhNjc3Y2ZjYjhhZmUyMmQwMjA4YzFlOGViZDVjNjIzYjY4ODBhODIzMmNhMTFlODYifQ%3D%3D'
};


j=1
path = './result/'
with open('links.pkl', 'rb') as f:
    links = pickle.load(f)
l = len(links)
for url in links:
    response = requests.get(url,headers=web_header)
    with open(os.path.join(path, os.path.basename(url)), 'wb') as f:
        f.write(response.content)
    print('one page finished! ' + str(j) + '/' + str(l))
    j += 1
print('All pages finished.')