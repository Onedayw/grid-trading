from collections import defaultdict, deque
from gevent.event import Event
from threading import Lock
from typing import DefaultDict, Deque, List, Dict

import sys
sys.path.append('.../')

from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from gateway.websocket_client import WebsocketClient


class BinanceSpotWebsocketClient(WebsocketClient):
    _ENDPOINT = 'wss://stream.binance.com:9443/'
    
    def __init__(self, on_message_cb, api_key: str = None, api_secret: str = None) -> None:
        self.ws_api_client = SpotWebsocketAPIClient(
            api_key=api_key,
            api_secret=api_secret,
            on_message=on_message_cb,
            on_close=self.on_close
        )


