from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dhan import Dhan
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL")
CLIENT_ID =  os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
D = Dhan(BASE_URL,CLIENT_ID, ACCESS_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        symbol = request.form['symbol']
        exchange = request.form['exchange']
        segment = "EQ"
        quantity = request.form['quantity']
        price = request.form['price']
        transactionType = request.form['transaction_type']
        orderType = "LIMIT"
        productType = "CNC"
        validity = "DAY"
        order_id = D.place_order(symbol,exchange,segment,transactionType,productType,orderType,validity,quantity,price)
        if isinstance(order_id, int):
            message = f"Order placed successfully with order ID: {order_id}"
            message_color = "success"
        else:
            message = order_id
            message_color = "warning"
        flash(message, message_color)
        return redirect(url_for('place_order'))
    else:
        exchanges = {"NSE","BSE","MCX"}
        return render_template('place_order.html',exchanges=exchanges)

@app.route('/holdings')
def holdings():
    holdings = D.get_holdings()
    data = holdings
    if not data:
        flash("Currently 0 Holdings",'warning')
        print("NO HOLDINGS")
    print(data)
    return render_template('holdings.html', holdings=data)

@app.route('/current_orders')
def current_orders():
    orders = D.get_orders_list()
    data = orders
    if not data:
        flash("Currently 0 Orders",'warning')
        print("NO CURRENT ORDERS")
    return render_template('current_orders.html', orders=data)


@app.route('/live_feed')
def live_feed():
    return render_template('live_feed.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")