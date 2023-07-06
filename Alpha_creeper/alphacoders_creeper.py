import alpha_url
import alpha_download

# ID='718'
# url = 'https://wall.alphacoders.com/by_collection.php?id='+ID+ '&quickload=230+&page='
#url = alpha_url.get_url_byapi('splatoon')
url = alpha_url.get_url('Naruto')
print(url)
alpha_download.download(url)