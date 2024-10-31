import sys
sys.path.append('.../')

import asyncio
from data_contract.enums import Platform
from gateway.client_factory import ClientFactory
from .long_grid_order_manager import LongGridOrderManager
from analytics.stat_manager import StatManager
from data_contract.enums import OrderSide, OrderStatus
from data_contract.order import Order
from logger.logger_config import logger


class LongGridTrader():
    def __init__(self, platform: Platform, symbol: str, start_price: float, num_of_grids: int, grid_interval: float, grid_volume: float) -> None:
        self.rest_client = ClientFactory.get_rest_client(platform)
        self.websocket_client = ClientFactory.get_websocket_client(self._on_message, platform)

        self.order_manager = LongGridOrderManager(symbol, start_price, num_of_grids, 3, grid_interval, grid_volume, self.rest_client.place_order)

        logger.info("Grid trading starts, start price: %f, grid prices for long:%s" % (
            self.order_manager.start_price,
            self.order_manager.grid_prices_long))

        def handle_socket_message(msg):
            #if msg['e'] == 'executionReport':
            print(f"message type: {msg['e']}")
            print(msg)
        
        self.websocket_client.start_user_socket(callback=handle_socket_message)
        
    async def run(self) -> None:
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
        self.websocket_client.user_data_start()

        # Keep the connection open
        while True:
            await asyncio.sleep(1)
    
    def _on_message(self, message):
        """
        Handle incoming WebSocket messages.
        """
        if message['e'] == 'executionReport':
            # update_order_status_in_db(order_id, status)
            order_id = message['i']
            status = OrderStatus(message['X'])
            side = OrderSide(message['S'])
            logger.info(f"Order ID: {order_id}, Status: {status}")
            
            if status == OrderStatus.FILLED:
                print(f"Order {order_id} has been filled.")
                # Perform some operations when the order is filled
                # Example: Log the filled order to a file
                logger.info(f"Order {order_id} filled at {message['T']} with price {message['L']} and quantity {message['l']}\n")
            
                # Update the order status in the database
                #update_order_status_in_db(order_id, status)
                
                # Place a new order to the next layer
                layer = self.order_manager.order_mapping.get(order_id)
                
                if side == OrderSide.BUY:
                    self.order_manager.place_sell_order(layer - 1)
                elif side == OrderSide.SELL:
                    self.order_manager.place_buy_order(layer + 1)

            elif status in [
                OrderStatus.CANCELED,
                OrderStatus.REJECTED,
                OrderStatus.EXPIRED,
                OrderStatus.PENDING_CANCEL,
                OrderStatus.EXPIRED_IN_MATCH]:
                logger.error(f"Status of order {order_id} is {status}.")
                # Perform some operations when the order is canceled
                # Example: Notify the user
                # notify_user(f"Order {order_id} has been canceled.")
            
            elif status == OrderStatus.NEW:
                logger.info(f"Order {order_id} is new.")
                # Perform some operations when the order is new
                # Example: Update the order status in the database
                # update_order_status_in_db(order_id, status)