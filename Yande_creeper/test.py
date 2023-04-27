from bs4 import BeautifulSoup
import requests as requests

web_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://yande.re/',
    'Connection': 'keep-alive',
    #'Cookie': '_pk_id.1.01b8=99da255d3e3d2c03.1681870764.; _pk_ses.1.01b8=1; XSRF-TOKEN=eyJpdiI6ImdnNmd4N3V2RVFSN0tZcEc0cGZkb0E9PSIsInZhbHVlIjoidTBZWmRmd3loZ0VGR3psN1hsOFlxNXh4ZnllZFFiUVZsK1lYU21lT2hqVmN3cEZBcUozV3hyWFZlWGppdzhROCIsIm1hYyI6IjFhMTIxZDBkYTNkZDA3MzZkNzQ1MDNiYWJhZmY5ZWQ0MjE1NDZkMWYzYzBiYWNkNmY0NmYxMWU2MjM1MzVjNDEifQ%3D%3D; wallhaven_session=eyJpdiI6ImlWM1N2Nm43MUtUU1hpakJHQVVLQUE9PSIsInZhbHVlIjoiQzMrV3ZUMkZhV09YSWdIb2JhM2dLZW5laEtQcExXbUZMSkZ6M2xSNm9XWHA3dDVTeXUzQmMrNG01dk1kRE1vaSIsIm1hYyI6IjYyZDVkNjU1NmQ0MDAwZDYxZTIwMDNhYjdkMzUzZGQ0YjQxOWJmZWRkNGMxMTkwYjFkNjRmOTQ1MjJlZjhkNmUifQ%3D%3D'
};

url = 'https://yande.re/post?page=1000&tags=bleach'
page = 1
urls = list()
req = requests.get(url=url, headers=web_header)
req.encoding = 'utf-8'
html_data = req.text
soup = BeautifulSoup(html_data, "html.parser")
links = soup.find_all('a', class_='directlink largeimg')
print(links)
