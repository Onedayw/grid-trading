import sys
import time
sys.path.append('../')

from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.ftx.rest_client import FtxRestClient
from termcolor import colored
from .neutral_grid_order_manager import NeutralGridOrderManager


class NeutralGridTrader:
    def __init__(self, start_price: float, num_of_grids: int, grid_interval: float, grid_volume: float, api_key: str=None, api_secret: str=None) -> None:
        self.rest_client = FtxRestClient(api_key, api_secret)
        self.order_manager = NeutralGridOrderManager(start_price, num_of_grids, 3, grid_interval, grid_volume, self.rest_client)

        self.websocket_client = FtxWebsocketClient(api_key, api_secret)
        self.websocket_client.connect()
        print(self.websocket_client.get_orders())

        print("Grid trading starts, start price: %f, trade volumes for long:%s, grid prices for long:%s, grid prices for short:%s" % (
            self.order_manager.start_price,
            self.order_manager.grid_volumes_long,
            self.order_manager.grid_prices_long,
            self.order_manager.grid_prices_short))

    def run(self, number_of_layers: int) -> None:
        while True:
            closed_orders = self.websocket_client.get_closed_order()

            if closed_orders:
                # TODO: handle multiple closed orders case
                layer = self.order_manager.order_mapping.get(closed_orders[-1]['id'], None)
                print('closed order layer is %d.' % (layer))
                if layer != None:
                    self.order_manager.place_buffer_orders(layer)
            #time.sleep(1)
