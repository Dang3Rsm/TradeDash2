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
        prdouctType = "CNC"
        validity = "DAY"
        exchange_segment = "BSE_EQ"
        order_id = D.place_order(symbol,exchange,segment,transactionType,prdouctType,orderType,validity,quantity,price)
        flash(f"Order placed successfully with order ID: {order_id}", "success")
        return redirect(url_for('place_order'))
    else:
        # Added some hardcoded values
        exchanges = {"NSE","BSE","MCX"}
        symbols = {
            "RELIANCE":500325,
            "TCS": 532540,
            "HDFCBANK": 500180,
            "INFY": 500209,
            "ICICIBANK": 532174,
            "SBIN": 500112,
            "HINDUNILVR": 500696,
            "AXISBANK": 532215
        }
        return render_template('place_order.html',symbols=symbols,exchanges=exchanges)

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
    app.run(debug=True)