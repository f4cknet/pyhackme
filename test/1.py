import mmh3
import requests
import base64

response = requests.get('https://bo.aichatme.com/favicon.ico')
favicon = base64.b64encode(response.content)
hash = mmh3.hash(favicon)
print('http.favicon.hash:'+str(hash))