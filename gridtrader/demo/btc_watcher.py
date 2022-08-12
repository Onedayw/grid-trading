import time
import sys
sys.path.append('../')

from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.ftx.rest_client import FtxRestClient

if __name__ == '__main__':
    api_key = 'PbjchxaHab7q6HOvsOuFVQ1fPy-UWLdxJjJhIpns'
    api_secret = 'pvPoQ-TOcvDyoljK1iqm_CJccUt1pl_RjV48GS1d'

    # ws = FtxWebsocketClient(api_key, api_secret)
    # ws.connect()
    # print('\n', ws.get_orderbook(market='ETH/USDT'))
    # ws.close()


    rest_client = FtxRestClient(api_key, api_secret)
    rest_client.place_order(
        market='ETH/USDT',
        side='buy',
        price=1920,
        type='limit',
        size=0.01,
    )
