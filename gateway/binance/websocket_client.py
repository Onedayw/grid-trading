import sys
sys.path.append('.../')

from api.websocket.websocket_client import WebsocketClient


class BinanceWebsocketClient(WebsocketClient):
    _ENDPOINT = 'wss://ws-api.binance.com:443/ws-api/v3'

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

    
    def _subscribe(self, subscription: Dict) -> None:
        self.send_json({'method': 'SUBSCRIBE', **subscription})
        self._subscriptions.append(subscription)
    
    def _unsubscribe(self, subscription: Dict) -> None:
        self.send_json({'method': 'UNSUBSCRIBE', **subscription})
        while subscription in self._subscriptions:
            self._subscriptions.remove(subscription)