import os
import pickle
import requests as requests

url = 'https://w.wallhaven.cc/full/1k/wallhaven-1k7ed9.jpg'
path = 'C:/personal data/wallheavn_creeper'
with open('links.pkl', 'rb') as f:
    links = pickle.load(f)
response = requests.get(links[0])
with open(os.path.join(path, os.path.basename(url)), 'wb') as f:
    f.write(response.content)
print(links[0])
