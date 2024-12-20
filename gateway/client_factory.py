import os
import sys
sys.path.append('.../')

from data_contract.enums import Platform
from gateway.binance.spot.rest_client import BinanceSpotRestClient
from gateway.binance.spot.websocket_client import BinanceSpotWebsocketClient
from gateway.binance.futures.rest_client import BinanceFuturesRestClient
from gateway.binance.futures.websocket_client import BinanceFuturesWebsocketClient
from gateway.ftx.rest_client import FtxRestClient
from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.rest_client import RestClient
from gateway.websocket_client import WebsocketClient


class ClientFactory:
    @staticmethod
    def get_rest_client(platform: Platform = Platform.FTX) -> RestClient:
        assert os.environ.get('API_KEY')
        assert os.environ.get('API_SECRET')

        api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')

        if platform == Platform.BINANCE_SPOT:
            return BinanceSpotRestClient(api_key, api_secret)
        elif platform == Platform.BINANCE_FUTURES:
            return BinanceFuturesRestClient(api_key, api_secret)
        else:
            return FtxRestClient(api_key, api_secret)

    @staticmethod
    def get_websocket_client(on_message_cb, platform: Platform = Platform.FTX) -> WebsocketClient:
        assert os.environ.get('API_KEY')
        assert os.environ.get('API_SECRET')

        api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')

        if platform == Platform.BINANCE_SPOT:
            return BinanceSpotWebsocketClient(on_message_cb, api_key, api_secret)
        elif platform == Platform.BINANCE_FUTURES:
            return BinanceFuturesWebsocketClient(api_key, api_secret)
        else:
            return FtxWebsocketClient(api_key, api_secret)