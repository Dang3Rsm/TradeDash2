import requests
import os
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
        #url = f'{self.base_url}/{endpoint}'
        url = self.base_url
        response = requests.request(method, url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint=None, payload=None):
        return self.req('POST', endpoint, data=payload)
    
    def place_order(self,symbol,transactionType,prdouctType,orderType,validity,quantity=0,price=0):
        securityId = self.get_security_data(symbol)
        exchangeSegment = self.get_security_data(symbol)
        payload = {
            "dhanClientId": self.client_id,
            "transactionType": transactionType,
            "exchangeSegment": exchangeSegment,
            "productType": prdouctType,
            "orderType": orderType,
            "validity": validity,
            "securityId": securityId,
            "quantity": quantity,
            "price": price,
        }
        response = D.req(method='POST',endpoint='/orders',payload=payload)
        order_id = response["orderId"]
        return order_id
    
    def get_holdings(self):
        response = D.req(method='GET',endpoint='/orders')
        return response

    def get_security_data(self,symbol):
        pass

if __name__ == "__main__":
    print("===EXECUTED===")

    BASE_URL = os.getenv("BASE_URL")
    print(BASE_URL)
    CLIENT_ID = os.getenv("CLIENT_ID")
    print(CLIENT_ID)
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    D = Dhan(BASE_URL,CLIENT_ID,ACCESS_TOKEN)
    #d = D.get_holdings()
    #print(d)
    print("===KILLED===")
