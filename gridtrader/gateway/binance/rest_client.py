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
