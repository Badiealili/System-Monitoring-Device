import requests
from bs4 import BeautifulSoup
import json

def get_latest_alert(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        alert = soup.find('div', class_='item cert-alert open')
        if alert:
            return alert.text.strip()


url = "https://www.cert.ssi.gouv.fr/"
alert = get_latest_alert(url)
data = [line for line in alert.split("\n") if line.strip()]

url+= 'alerte/' + data[1]

obj = {
    "date": data[0],
    "id":data[1],
    "url":url,
    "title":data[2],
    "status":data[3]
}

with open('latest-alert.json', 'w') as file:
    file.write(json.dumps(obj))