import hmac
import time
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
    
    def __init__(self, api_key: str = None, api_secret: str = None) -> None:
        super().__init__()
        self._trades: DefaultDict[str, Deque] = defaultdict(lambda: deque([], maxlen=10000))
        self._fills: Deque = deque([], maxlen=10000)
        self._api_key = api_key
        self._api_secret = api_secret
        self._orderbook_update_events: DefaultDict[str, Event] = defaultdict(Event)
        self._lock = Lock()
        self._reset_data()

    def _on_open(self, ws):
        self._reset_data()

    def _reset_data(self) -> None:
        self._subscriptions: List[Dict] = []
        self._orders: DefaultDict[int, Dict] = defaultdict(dict)
        self._closed_orders: List[Dict] = []
        self._tickers: DefaultDict[str, Dict] = defaultdict(dict)
        self._orderbook_timestamps: DefaultDict[str, float] = defaultdict(float)
        self._orderbook_update_events.clear()
        self._orderbooks: DefaultDict[str, Dict[str, DefaultDict[float, float]]] = defaultdict(
            lambda: {side: defaultdict(float) for side in {'bids', 'asks'}})
        self._orderbook_timestamps.clear()
        self._logged_in = False
        self._last_received_orderbook_data_at: float = 0.0
    
    def _login(self) -> None:
        ts = int(time.time() * 1000)
        self.send_json({'op': 'login', 'args': {
            'key': self._api_key,
            'sign': hmac.new(
                self._api_secret.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest(),
            'time': ts,
        }})
        self._logged_in = True

    def _subscribe(self, subscription: Dict) -> None:
        self.send_json({'op': 'subscribe', **subscription})
        self._subscriptions.append(subscription)

    def _unsubscribe(self, subscription: Dict) -> None:
        self.send_json({'op': 'unsubscribe', **subscription})
        while subscription in self._subscriptions:
            self._subscriptions.remove(subscription)
    
    def get_closed_order(self) -> List[Dict]:
        if not self._logged_in:
            self._login()
        subscription = {'channel': 'orders'}
        if subscription not in self._subscriptions:
            self._subscribe(subscription)
        self._lock.acquire()
        res = self._closed_orders.copy()
        self._closed_orders = []
        self._lock.release()
        return res