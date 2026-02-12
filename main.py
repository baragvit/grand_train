import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from html_fetcher import get_grand_train_page


def send_notification_via_bot(message):
    chat_id = os.environ['TELEGRAM_CHANNEL_ID']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}.'
    response = requests.get(telegram_url)
    response.raise_for_status()


def has_tickets(html):
    soup = BeautifulSoup(html, "lxml")
    kupe_carriages = soup.findAll(attrs={"data-filter": "Купе"})
    for carriage in kupe_carriages:
        invalid = carriage.find("div", class_="car-class__note-main")
        if invalid and 'Купе для маломобильных пассажиров' in invalid.text:
            continue
        places = carriage.findAll("div", class_="car-class__fare-item")
        if (len([s.find('span') for s in places if 'нижн' in s.find('span').text])):
            return True


def main():
    load_dotenv()
    attempts = 0
    timeout_exceptions = 0
    send_notification_via_bot("Начинаем мониторить")
    while True:
        try:
            result = get_grand_train_page()
            if "ok" in result and has_tickets(result["ok"]):
                send_notification_via_bot("Есть места ")
                time.sleep(600)
            attempts += 1
            if attempts % 1000 == 0:
                send_notification_via_bot(f"Бот жив, продолжает вести наблюдение, попыток {attempts}")
            if "failed" in result:
                timeout_exceptions += 1
                if timeout_exceptions % 1000 == 0:
                    send_notification_via_bot(f"{timeout_exceptions} time out exceptions")
            time.sleep(60)
        except Exception as e:
            send_notification_via_bot(str(e))
            time.sleep(60)


if __name__ == '__main__':
    main()
