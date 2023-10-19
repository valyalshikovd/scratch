from bs4 import BeautifulSoup
import fake_useragent
import requests

def scratch():
    url = "https://www.cs.vsu.ru/brs/login"
    data = {
        'login': '---',
        'password': '---',
        'button_login': 'Вход'
    }
    user = fake_useragent.UserAgent.random
    # header = {
    #     'user-agent': user
    # }
    headers = {
        "Accept": "*/*",
        "User-Agent": " --- "
    }
   # request = requests.get(url, headers=header)
    responce = requests.post(url, data=data, headers=headers).text
    print(responce)
    with open("index.html", "w", encoding="utf-8-sig") as file:
        file.write(responce)