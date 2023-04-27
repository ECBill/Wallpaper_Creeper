import pickle
from bs4 import BeautifulSoup
import requests as requests

web_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://wallhaven.cc/',
    'Connection': 'keep-alive',
    'Cookie': '_pk_id.1.01b8=99da255d3e3d2c03.1681870764.; _pk_ses.1.01b8=1; XSRF-TOKEN=eyJpdiI6ImdnNmd4N3V2RVFSN0tZcEc0cGZkb0E9PSIsInZhbHVlIjoidTBZWmRmd3loZ0VGR3psN1hsOFlxNXh4ZnllZFFiUVZsK1lYU21lT2hqVmN3cEZBcUozV3hyWFZlWGppdzhROCIsIm1hYyI6IjFhMTIxZDBkYTNkZDA3MzZkNzQ1MDNiYWJhZmY5ZWQ0MjE1NDZkMWYzYzBiYWNkNmY0NmYxMWU2MjM1MzVjNDEifQ%3D%3D; wallhaven_session=eyJpdiI6ImlWM1N2Nm43MUtUU1hpakJHQVVLQUE9PSIsInZhbHVlIjoiQzMrV3ZUMkZhV09YSWdIb2JhM2dLZW5laEtQcExXbUZMSkZ6M2xSNm9XWHA3dDVTeXUzQmMrNG01dk1kRE1vaSIsIm1hYyI6IjYyZDVkNjU1NmQ0MDAwZDYxZTIwMDNhYjdkMzUzZGQ0YjQxOWJmZWRkNGMxMTkwYjFkNjRmOTQ1MjJlZjhkNmUifQ%3D%3D'
};

url = 'https://wallhaven.cc/search?q=zootopia&page='
page=1
urls = list()
while True:
    url_n = url+str(page)
    req = requests.get(url=url_n, headers=web_header);
    req.encoding = 'utf-8'
    html_data = req.text
    soup = BeautifulSoup(html_data, "html.parser")
    links = soup.find_all('a', class_='preview')
    if links == []:
        break
    for link in links:
        urls.append(link.get('href'))
    page+=1
links = list()
for url in urls:
    req = requests.get(url=url, headers=web_header)
    req.encoding = 'utf-8'
    html_data = req.text
    soup = BeautifulSoup(html_data, "html.parser")
    img = soup.find('img', id='wallpaper')
    while img==None:
        req = requests.get(url=url, headers=web_header)
        req.encoding = 'utf-8'
        html_data = req.text
        soup = BeautifulSoup(html_data, "html.parser")
        img = soup.find('img', id='wallpaper')
    src = img.get('src')
    links.append(src)
l = len(urls)
print(links)
with open('links.pkl', 'wb') as f:
    pickle.dump(links, f)
