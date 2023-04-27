import alpha_url
import alpha_download

url = alpha_url.get_url('zootopia')
print(url)
alpha_download.download(url)