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