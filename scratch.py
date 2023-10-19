from bs4 import BeautifulSoup
import fake_useragent
import requests
import re
from Subj import Subj


def scratch():
    ##url = "https://www.cs.vsu.ru/brs/login"

    data = {
        'login': 'valyalschikov_d_a',
        'password': 'vsu1140_',
        'button_login': 'Вход'
    }

    # user = fake_useragent.UserAgent.random
    # header = {
    #     'user-agent': user
    # }

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    #   responce = requests.post(url, data=data, headers=headers).text --- это

    with open('index.html', encoding="utf-8-sig") as file:
        f = file.read()

    soup = BeautifulSoup(f, "lxml")
    table = soup.find("table")
    marks = table.find_all('tr')
    subjects_as_object = []
    for subj in marks:
        modified_items = []
        for f in subj.find_all("td"):
            modified_items.append(f.text.replace("\n", '').strip())
        if len(modified_items) < 12:
            continue
        subjects_as_object.append(
            Subj(modified_items[0], modified_items[1], modified_items[2], modified_items[3], modified_items[4],
                 modified_items[5], modified_items[6], modified_items[7], modified_items[8], modified_items[9],
                 modified_items[10], modified_items[11],
                 modified_items[12]))
    for s in subjects_as_object:
        print(s.to_string())
