from bs4 import BeautifulSoup
import fake_useragent
import requests
import re
from Subj import Subj


def scratch(login, password):
    url = "https://www.cs.vsu.ru/brs/login"
    data = {
        'login': login,
        'password': password,
        'button_login': 'Вход'
    }
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    responce = requests.post(url, data=data, headers=headers).text
    soup = BeautifulSoup(responce, "lxml")
    if soup.find(class_="col-sm-4 d-block invalid-feedback") is not None:
        raise ConnectionError('')
    table = soup.find("table")
    marks = table.find_all('tr')
    subjects_as_object = []
    for subj in marks:
        modified_items = []
        for f in subj.find_all("td"):
            modified_items.append(f.text.replace("\n", '').strip())
        modified_items.append(subj.find("th").text.replace("\n", '').strip())
        if len(modified_items) < 14:
            continue
        subjects_as_object.append(
            Subj(modified_items[0], modified_items[1], modified_items[2], modified_items[3], modified_items[4],
                 modified_items[5], modified_items[6], modified_items[7], modified_items[8], modified_items[9],
                 modified_items[10], modified_items[11],
                 modified_items[13]))
    return subjects_as_object
