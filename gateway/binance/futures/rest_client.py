import sys
sys.path.append('.../')

from binance.um_futures import UMFutures as Client
from gateway.rest_client import RestClient


class BinanceFuturesRestClient(RestClient):
    _ENDPOINT = 'https://fapi.binance.com/'

    def __init__(self, api_key: str=None, api_secret: str=None) -> None:
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self._api_key = api_key
        self._api_secret = api_secret