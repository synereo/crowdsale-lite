import requests

from app import db, Transaction
from datetime import datetime
from os import environ
from pytz import utc


def get_coindesk_rate():
    TICKER_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    ticker = requests.get(TICKER_URL)
    rate = ticker.json()['bpi']['USD']['rate_float']
    return rate


def parse_tx(btc_addr, tx, usd_rate):
    if 'block_height' not in tx:
        # skip this TX, it's unverified
        return

    for inpt in tx['inputs']:
        if inpt['prev_out']['addr'] == btc_addr:
            # skip change transactions
            return

    hash_id = tx['hash']
    block_height = tx['block_height']

    time = datetime.fromtimestamp(tx['time'], tz=utc)
    amount = sum([x['value'] for x in tx['out'] if x['addr'] == btc_addr])
    usd_worth = float(usd_rate) * obj.amount / 10e7

    dbtx = Transaction.query.filter_by(hash_id=hash_id).first()
    if not dbtx:
        dbtx = Transaction(hash_id=hash_id, block_height=block_height, time=time, amount=amount, usd_worth=usd_worth)
        db.session.add(dbtx)
        db.session.commit()


def get_blockchain_txs(usd_rate):
    ADDRESS_URL = 'https://blockchain.info/address/{}'
    BTC_ADDR = environ.get('BTC_ADDR')

    res = requests.get(ADDRESS_URL.format(BTC_ADDR), params={'format': 'json'})
    for tx in res.json()['txs']:
        parse_tx(BTC_ADDR, tx, usd_rate)


print('Starting update.py')

usd_rate = get_coindesk_rate()
print('Current coindesk BTC/USD rate: ${}'.format(usd_rate))

get_blockchain_txs(usd_rate)

print('Done.')
