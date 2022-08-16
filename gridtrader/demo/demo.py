import time
import sys
sys.path.append('../')

from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.ftx.rest_client import FtxRestClient

if __name__ == '__main__':
    api_key = '<API KEY>'
    api_secret = '<API SECRET>'

    ws = FtxWebsocketClient(api_key, api_secret)
    ws.connect()
    print('\n', ws.get_orderbook(market='ETH/USDT'))
    ws.close()

    rest_client = FtxRestClient(api_key, api_secret)
    response = rest_client.place_order(
        market='ETH/USDT',
        side='sell',
        price=1930,
        type='limit',
        size=0.01,
    )

    print(response)
