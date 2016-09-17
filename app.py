import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_id = db.Column(db.String(64), unique=True)
    sender = db.Column(db.String(35))
    block_height = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    amount = db.Column(db.BigInteger)
    usd_worth = db.Column(db.Float)

    def __init__(self, hash_id, sender, block_height, time, amount, usd_worth):
        self.hash_id = hash_id
        self.sender = sender
        self.block_height = block_height
        self.time = time
        self.amount = amount
        self.usd_worth = usd_worth

    def __repr__(self):
        return '<Transaction %r>' % self.hash_id


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
