import sys
import time
sys.path.append('.../')

from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.ftx.rest_client import FtxRestClient
from termcolor import colored
from .long_grid_order_manager import LongGridOrderManager
from analytics.stat_manager import StatManager
from data_contract.order import Order
from logger.logger_config import logger


class LongGridTrader():
    def __init__(self, symbol: str, start_price: float, num_of_grids: int, grid_interval: float, grid_volume: float, api_key: str=None, api_secret: str=None) -> None:
        # TODO: Use factory pattern to instantiate a rest client
        self.rest_client = FtxRestClient(api_key, api_secret)
        self.order_manager = LongGridOrderManager(symbol, start_price, num_of_grids, 3, grid_interval, grid_volume, self.rest_client)
        start_balance = self.rest_client.get_total_account_usd_balance()
        self.stat_manager = StatManager(start_balance)

        self.websocket_client = FtxWebsocketClient(api_key, api_secret)
        self.websocket_client.connect()

        logger.info("Grid trading starts, start price: %f, grid prices for long:%s" % (
            self.order_manager.start_price,
            self.order_manager.grid_prices_long))
        
    def run(self, number_of_layers: int) -> None:
        while True:
            closed_orders = self.websocket_client.get_closed_order()

            if closed_orders:
                # TODO: handle multiple closed orders case
                self.stat_manager.add_closed_order(Order(closed_orders[-1]))
                layer = self.order_manager.order_mapping.get(closed_orders[-1]['id'], None)
                logger.info('The closed order layer is %d.' % (layer))
                balance = self.rest_client.get_total_account_usd_balance()
                total_profit = self.stat_manager.get_total_profit(balance)
                logger.info('Total gain is %f.' % total_profit)
                grid_profit = self.stat_manager.get_grid_profit()
                logger.info('Grid gain is %f.' % grid_profit)
                logger.info('Market gain is %f.' % (total_profit - grid_profit))
                if layer != None:
                    self.order_manager.place_buffer_orders(layer)
            #time.sleep(1)
            