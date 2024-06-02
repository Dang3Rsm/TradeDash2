import asyncio
import websockets
import struct
import os
from dotenv import load_dotenv

load_dotenv()

WSS_URL = 'wss://api-feed.dhan.co'
IDX, NSE, NSE_FNO, NSE_CURR, BSE, MCX, BSE_CURR, BSE_FNO = range(8)
Ticker, Quote, Depth = 15, 17, 19

class MarketFeed:
    def __init__(self, client_id, access_token, instruments, subscription_code):
        self.client_id = client_id
        self.access_token = access_token
        self.instruments = instruments
        self.subscription_code = subscription_code

    async def connect(self):
        async with websockets.connect(WSS_URL) as ws:
            await self.authorize(ws)
            await self.subscribe_instruments(ws)
            async for message in ws:
                print("Received:", message)

    async def authorize(self, ws):
        api_access_token = self.access_token.ljust(500, '\0').encode('utf-8')
        authentication_type = "2P".encode('utf-8')
        payload = api_access_token + authentication_type
        header = struct.pack('<bH30s50s', 11, 83 + len(payload), self.client_id.ljust(30, '\0').encode('utf-8'), b"\0" * 50)
        authorization_packet = header + payload
        await ws.send(authorization_packet)

    async def subscribe_instruments(self, ws):
        num_instruments = len(self.instruments)
        header = struct.pack('<bH30s50s', self.subscription_code, 83 + 4 + num_instruments * 21,
                             self.client_id.ljust(30, '\0').encode('utf-8'), b"\0" * 50)
        num_instruments_bytes = struct.pack('<I', num_instruments)
        instrument_info = b"".join(struct.pack('<B20s', exchange_segment, security_id.encode('utf-8')) for exchange_segment, security_id in self.instruments)
        instrument_info += b"".join(struct.pack('<B20s', 0, b"") for _ in range(100 - num_instruments))
        subscription_packet = header + num_instruments_bytes + instrument_info
        await ws.send(subscription_packet)

if __name__ == "__main__":
    CLIENT_ID = os.getenv("CLIENT_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    instruments = [(NSE, "1333"), (IDX, "13")]  # Dummy data to subscribe
    subscription_code = Ticker
    
    feed = MarketFeed(CLIENT_ID, ACCESS_TOKEN, instruments, subscription_code)
    asyncio.run(feed.connect())