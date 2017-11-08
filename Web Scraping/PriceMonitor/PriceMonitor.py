from bs4 import BeautifulSoup
import time
from datetime import datetime
import requests
import pandas as pd
import urllib
import re

import smtplib
from email.mime.text import MIMEText

# Set up parameters
PRODUCT_URL = '''https://www.amazon.com/Dell-27-Inch-LED-lit-Monitor-U2718Q/dp/B073VYVX5S/ref
=sr_1_5?ie=UTF8&qid=1510103212&sr=8-5&keywords=dell+4k+monitor'''

RECEIVER = "@gmail.com"
SENDER = '@gmail.com'
MY_PASSWORD = '********'  # Keep it secure

DESIRED_PRICE = 500.00  # in dollar
REQUEST_FREQUENCY = 30  # in second

log_file = 'price_log.txt'  # Keep a local copy of price history


'''Check price with given REQUEST_FREQUENCY.'''


def get_price(product_url):
    while True:
        response = requests.get(product_url)
        html = response.text.encode('utf-8')
        page_soup = BeautifulSoup(html, "lxml")

        price_block = page_soup.find('span', {'id': 'priceblock_ourprice'})
        if price_block:
            price = float(price_block.text.strip()[1:])
            with open(log_file, 'a') as log:  # append mode instead of overwriting the data
                message = str(datetime.now()) + ': $' + str(price) + '\n'
                log.write(message)
            if price <= DESIRED_PRICE:
                send_mail(price, product_url)
                print('Email sent!')  # debug
                time.sleep(REQUEST_FREQUENCY * 10)  # slow down here once the price drops

        print('im sleeping')
        time.sleep(REQUEST_FREQUENCY)


'''Send email with current price included, keeping a record of the prices'''


def send_mail(price, product_url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    content = 'The price of the product falls in your desired range. The current price is ' + str(
        price) + '\nProduct link: ' + product_url

    msg = MIMEText(content)
    msg['Subject'] = 'Price Alert'
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    server.login(SENDER, MY_PASSWORD)
    server.sendmail(SENDER, RECEIVER, msg.as_string())
    server.quit()


def main(): get_price(PRODUCT_URL)

if __name__ == "__main__": main()
