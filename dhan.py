import requests
import os
import sqlite3
from dotenv import load_dotenv
class Dhan:
    def __init__(self, base_url, client_id, access_token):
        self.base_url = base_url
        self.access_token = access_token
        self.client_id = client_id

    def req(self, method, endpoint=None, payload=None):
        headers = {
            "access-token": self.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        url = f'{self.base_url}{endpoint}'
        #url = self.base_url
        response = requests.request(method, url, json=payload, headers=headers)
        # response.raise_for_status()
        return response.json()

    def post(self, endpoint=None, payload=None):
        return self.req('POST', endpoint, data=payload)
    
    def place_order(self,symbol,exchange,segment,transactionType,productType,orderType,validity,quantity=0,price=0):
        securityId = self.get_security_data(symbol,exchange)
        exchangeSegment = exchange + "_"+segment
        payload = {
            "dhanClientId": self.client_id,
            "transactionType": transactionType,
            "exchangeSegment": exchangeSegment,
            "productType": productType,
            "orderType": orderType,
            "validity": validity,
            "securityId": securityId,
            "quantity": quantity,
            "price": price
        }
        response = self.req(method='POST',endpoint='/orders',payload=payload)
        if 'orderId' in response:
            return response["orderId"]
        else:
            return response.get('internalErrorMessage')
    
    def get_orders_list(self):
        response = self.req(method='GET',endpoint='/orders')
        return response

    def get_holdings(self):
        response = self.req(method='GET',endpoint='/holdings')
        return response
    
    def get_positions(self):
        response = self.req(method='GET',endpoint='/positions')
        return response

    def connectScripDB(self):
        return sqlite3.connect("scripDB.sqlite3")

    def get_security_data(self, symbol,exchange):
        conn = self.connectScripDB()
        cursor = conn.cursor()
        cursor.execute("SELECT SEM_EXM_EXCH_ID, SEM_SMST_SECURITY_ID FROM scrip_master_table WHERE SEM_TRADING_SYMBOL=?", (symbol,))
        data = cursor.fetchall()
        conn.close()
        data = set(data)        # remove duplicates
        data = dict(data)       # easy accesss for keys
        try:
            data = data[exchange]
        except KeyError:
            data = None
        return data
    
    def get_unique_symbols(self,exchange):
        conn = self.connectScripDB()
        cursor = conn.cursor()
        cursor.execute("SELECT SEM_TRADING_SYMBOL FROM scrip_master_table WHERE SEM_EXM_EXCH_ID=?", (exchange,))
        data = cursor.fetchall()
        conn.close()
        data = set(data)        # remove duplicates
        data = list(data)       # list of symbols
        return None

if __name__ == "__main__":
    print("===EXECUTED===")

    load_dotenv()
    BASE_URL = os.getenv("BASE_URL")
    CLIENT_ID = os.getenv("CLIENT_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    D = Dhan(BASE_URL,CLIENT_ID,ACCESS_TOKEN)
    d = None
    # d = D.get_holdings()
    # d = D.get_positions()
    # d = D.get_security_data("SBIN","BSE")
    # d = D.place_order("SBIN","NSE","EQ","BUY","CNC","LIMIT","DAY",quantity=1,price=2000)
    # d = D.get_unique_symbols("NSE")
    # d = D.get_orders_list()
    print(d)
    print("===KILLED===")
