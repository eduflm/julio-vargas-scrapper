from datetime import datetime
import requests
from bs4 import BeautifulSoup
import telegram_send
import time
import datetime
import json


INTERVAL_TO_SCRAP = 600000
MAX_NOTIFY_ALIVE = 6



def log_in(credentials):
    url = credentials["main_link"]
    values = {'sle_sLogin': credentials["sle_sLogin"],
            'sle_sSenha': credentials["sle_sSenha"]
            }

    s = requests.session()

    r = s.post(url, data=values)
    r2 = s.get(credentials["laudo_link"])

    return r2.text

def get_value_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    spans = soup.find_all("span", id="dwTableFormat")
    return spans[2].text

def send_success_message():
    telegram_send.send(messages=["Temos um resultado do exame!"])

def send_alive_message():
    telegram_send.send(messages=["O resultado do exame ainda não foi modificado!"])

def get_credentials():
    file = open('credentials.json')
    data = json.load(file)
    return data


if __name__ == "__main__":
    current_notification = 0
    while True:
        print("Scraping...") 
        print("Scrap Time:", datetime.datetime.now())
        print("Current Notification: ", current_notification) 
        credentials = get_credentials()
        request_content = log_in(credentials)
        value = get_value_from_html(request_content)
        print("Current Value: ", value)
        if value != 'Em execução':
            send_success_message()
        
        if current_notification >= MAX_NOTIFY_ALIVE:
            send_alive_message()
            current_notification = 0
        else:
            current_notification = current_notification + 1

        print("Sleeping....")
        time.sleep(INTERVAL_TO_SCRAP)
 