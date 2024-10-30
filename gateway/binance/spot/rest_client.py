import sys
from typing import List
sys.path.append('.../')

from binance.spot import Spot as Client
from gateway.rest_client import RestClient


class BinanceSpotRestClient(RestClient):
    _ENDPOINT = 'https://api.binance.com/'

    def __init__(self, api_key: str=None, api_secret: str=None) -> None:
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self._api_key = api_key
        self._api_secret = api_secret

    def get_markets(self) -> list:
        return self.client.exchange_info()
    
    def get_orderbook(self, market: str, depth: int=None) -> dict:
        return self.client.depth(symbol=market, limit=depth)
    
    def get_trades(self, market: str, start_time: float=None, end_time: float=None) -> dict:
        return self.client.trades(symbol=market, startTime=start_time, endTime=end_time)
    
    def get_account_info(self) -> dict:
        return self.client.account()
    
    def get_open_orders(self, market: str=None) -> list:
        return self.client.open_orders(symbol=market)
    
    def get_order_history(self, market: str=None, side: str=None, order_type: str=None, start_time: float=None, end_time: float=None) -> list:
        return self.client.my_trades(symbol=market, startTime=start_time, endTime=end_time)
    
    def modify_order(self, existing_order_id: str=None, existing_client_order_id: str=None, price: float=None, size: float=None, client_order_id: str=None) -> dict:
        params = {
            'symbol': existing_order_id,
            'orderId': existing_client_order_id,
            'price': price,
            'quantity': size,
            'newClientOrderId': client_order_id
        }
        return self.client.new_order(**params)
    
    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit', 
                    reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    client_id: str = None, reject_after_ts: float = None) -> dict:

        return self.client.new_order(
            symbol=market,
            side=side,
            type=type,
            quantity=size,
            price=price,
            timeInForce='GTC'
        )
    
    def cancel_order(self, market: str, order_id: int=None) -> dict:
        return self.client.cancel_order(symbol=market, orderId=order_id)

    def cancel_orders(self, market: str) -> dict:
        return self.client.cancel_open_orders(symbol=market)
    
    def get_fills(self, market: str=None, start_time: float=None, end_time: float=None, min_id: int=None, order_id: int=None) -> list:
        return self.client.my_trades(symbol=market, startTime=start_time, endTime=end_time, fromId=min_id, orderId=order_id)
    
    def get_balances(self) -> List[dict]:
        return self.client.account()['balances']
            
    def get_total_account_usd_balance(self) -> float:
        return self.client.balance()
    
    def get_all_balances(self) -> List[dict]:
        return self.client.balance()
    
    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        # TODO: Implement this method
        return None
    
    def get_position(self, name: str, show_avg_price: bool = False) -> dict:
        # TODO: Implement this method
        return None
    
    def get_all_trades(self, market: str, start_time: float = None, end_time: float = None) -> List:
        return self.client.my_trades(symbol=market, startTime=start_time, endTime=end_time)