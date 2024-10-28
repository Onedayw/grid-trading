import sys
sys.path.append('.../')

from binance.spot import Spot as Client
from gateway.rest_client import RestClient


class BinanceSpotRestClient(RestClient):
    _ENDPOINT = 'https://api.binance.com/'

    def __init__(self, api_key: str=None, api_secret: str=None) -> None:
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self._api_key = api_key
        self._api_secret = api_secret
        
    def get_total_account_usd_balance(self) -> float:
        account_info = self.client.get_account()
        for balance in account_info['balances']:
            if balance['asset'] == 'USDT':
                return float(balance['free'])
        return 0.0