import requests

from app import db, Transaction

def get_coindesk_rate():
    TICKER_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    ticker = requests.get(TICKER_URL)
    rate = ticker.json()['bpi']['USD']['rate_float']
    return rate

print('Starting update.py')

print('Current coindesk BTC/USD rate: ${}'.format(get_coindesk_rate()))

