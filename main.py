from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dhan import Dhan

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CLIENT_ID =  os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
D = Dhan(CLIENT_ID, ACCESS_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        symbol = request.form['symbol']
        quantity = request.form['quantity']
        price = request.form['price']
        transaction_type = request.form['transaction_type']
        security_id = request.form['security_id']
        order_type = "LIMIT"
        product_type = "CNC"
        validity = "DAY"
        exchange_segment = "BSE_EQ"
        data = D.place_order(
            security_id, exchange_segment, transaction_type,
            int(quantity), order_type, product_type, float(price), validity
        )

        if data['status'] == 'failure':
            flash("Failed to place the order.", "danger")
        else:
            order_id = data['data']['orderId']
            flash(f"Order placed successfully with order ID: {order_id}", "success")

        return redirect(url_for('place_order'))
    else:
        # Added some hardcoded values
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

        return render_template('place_order.html',symbols=symbols)

@app.route('/holdings')
def holdings():
    holdings = D.get_holdings()
    data = holdings['data']
    if not data:
        flash("Currently 0 Holdings",'warning')
        print("NO HOLDINGS")
    print(data)
    return render_template('holdings.html', holdings=data)


@app.route('/live_feed')
def live_feed():
    return render_template('live_feed.html')

if __name__ == '__main__':
    app.run(debug=True)