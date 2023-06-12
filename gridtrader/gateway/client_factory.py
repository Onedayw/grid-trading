import os
import sys
sys.path.append('.../')

from data_contract.enums import Platform
from gateway.rest_client import RestClient
from gateway.binance.rest_client import BinanceRestClient
from gateway.ftx.rest_client import FtxRestClient


class ClientFactory:
    @staticmethod
    def get_rest_client(platform: Platform = Platform.BINANCE) -> RestClient:
        assert not os.environ.get('API_KEY')
        assert not os.environ.get('API_SECRET')

        api_key, api_secret = os.environ.get('API_KEY'), os.environ.get('API_SECRET')

        if platform == Platform.BINANCE:
            return BinanceRestClient(api_key, api_secret)
        else:
            return FtxRestClient(api_key, api_secret)
