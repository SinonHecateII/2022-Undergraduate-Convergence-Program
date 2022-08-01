import pymysql
import ImportantData
import requests

r = requests.post('https://github.com/login/oauth/access_token')
print(r.text)
