import sys
sys.path.append('.../')

from data_contract.enums import Platform
from gateway.client_factory import ClientFactory
from gateway.websocket_client import WebsocketClient
from .long_grid_order_manager import LongGridOrderManager
from analytics.stat_manager import StatManager
from data_contract.order import Order
from logger.logger_config import logger


class LongGridTrader():
    def __init__(self, platform: Platform, symbol: str, start_price: float, num_of_grids: int, grid_interval: float, grid_volume: float) -> None:
        self.rest_client = ClientFactory.get_rest_client(platform)
        self.websocket_client = ClientFactory.get_websocket_client(platform)

        self.order_manager = LongGridOrderManager(symbol, start_price, num_of_grids, 3, grid_interval, grid_volume, self.client.create_order)


        self.websocket_client = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        self.websocket_client.start()

        logger.info("Grid trading starts, start price: %f, grid prices for long:%s" % (
            self.order_manager.start_price,
            self.order_manager.grid_prices_long))

        def handle_socket_message(msg):
            #if msg['e'] == 'executionReport':
            print(f"message type: {msg['e']}")
            print(msg)
        
        self.websocket_client.start_user_socket(callback=handle_socket_message)
        
    def run(self) -> None:
        '''
        # Strategy for moving upper and lower grid boundaries
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
            time.sleep(1)
        '''

        # Strategy for fixed upper and lower grid boundaries
        while True:

            