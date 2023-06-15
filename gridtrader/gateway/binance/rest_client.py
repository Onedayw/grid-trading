import sys
sys.path.append('.../')

from gateway.rest_client import RestClient
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

class BinanceRestClient(RestClient):
    _ENDPOINT = 'https://api.binance.us/api/'

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
    requests_params: Optional[Dict[str, str]] = None, tld: str = 'com', testnet: bool = False) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name
        self._client = Client(api_key, api_secret)

    def get_all_futures(self) -> List[dict]:
        pass

    def get_future(self, future_name: str = None) -> dict:
        pass

    def get_markets(self) -> List[dict]:
        pass

    def get_orderbook(self, market: str, depth: int = None) -> dict:
        return self._client.get_order_book(symbol=market)

    def get_trades(self, market: str, start_time: float = None, end_time: float = None) -> dict:
        return self._client.get_recent_trades(symbol=market)

    def get_account_info(self) -> dict:
        pass

    def get_open_orders(self, market: str = None) -> List[dict]:
        pass 

    def get_order_history(
        self, market: str = None, side: str = None, order_type: str = None,
        start_time: float = None, end_time: float = None
    ) -> List[dict]:
        pass

    def modify_order(
        self, existing_order_id: Optional[str] = None,
        existing_client_order_id: Optional[str] = None, price: Optional[float] = None,
        size: Optional[float] = None, client_order_id: Optional[str] = None,
    ) -> dict:
        pass

    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit',
                    reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    client_id: str = None, reject_after_ts: float = None) -> dict:
        pass

    def cancel_order(self, order_id: str) -> dict:
        pass

    def cancel_orders(
        self, market_name: str = None,
        conditional_orders: bool = False, limit_orders: bool = False) -> dict:
        pass

    def get_fills(
        self, market: str = None, start_time: float = None,
        end_time: float = None, min_id: int = None, order_id: int = None) -> List[dict]:
        pass

    def get_balances(self) -> List[dict]:
        pass

    def get_all_balances(self) -> List[dict]:
        pass

    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        pass

    def get_position(self, name: str, show_avg_price: bool = False) -> dict:
        pass

    def get_all_trades(self, market: str, start_time: float = None, end_time: float = None) -> List:
        pass
