import time
import sys
sys.path.append('../')

from gateway.ftx.ftx_client import FtxWebsocketClient, FtxRestClient

if __name__ == '__main__':
    api_key = 'SXiAWmog3-E35O6O2XkRyT7Y8XDuA5IF2P_wEwO1'
    api_secret = '_JMA1kJvL7_Px0GyooVGcLldxKhQhuI2l-4Zt4BB'
    # ws = FtxWebsocketClient(api_key, api_secret)
    # ws.connect()
    # while True:
    #     print('\n', ws.get_orderbook(market='BTC-PERP'))
    #     time.sleep(1)

    rest_client =
