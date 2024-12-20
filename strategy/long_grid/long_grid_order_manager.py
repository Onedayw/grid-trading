import sys
sys.path.append('.../')

from functools import reduce
from typing import List

from data_contract.order import Order
from data_contract.enums import OrderStatus
from logger.logger_config import logger


class LongGridOrderManager:
    def __init__(self, symbol: str, start_price: float, num_of_layers: int, grid_buffer: int,
        grid_interval: float, grid_volume: float, cb) -> None:
        self.symbol = symbol
        self.start_price = start_price
        self.num_of_layers = num_of_layers
        self.grid_buffer = grid_buffer
        self.grid_interval = grid_interval
        self.grid_volume = grid_volume
        self.place_order_cb = cb

        self.grid_region_long = [self.grid_interval] * self.num_of_layers  # price intervals for long (grid density)

        max_price = self.start_price
        for i in range(int(self.num_of_layers/2)):
            max_price = max_price / (1 - self.grid_region_long[i])

        self.grid_prices_long = [reduce(lambda p, r: p*(1-r), self.grid_region_long[:i], max_price) for i in range(self.num_of_layers + 1)]  # gride prices for long
        print(self.grid_prices_long)
        self.last_filled_order = None
        self._init_orders()

    def _init_orders(self) -> None:
        """
        Place initial limit orders
        """
        self.orders = [None] * (self.num_of_layers + 1)
        self.order_mapping = {}
        layer = self.get_layer_num(self.start_price) - 1
        self.place_buffer_orders(self.symbol, layer)

    def _clean_up_order_with_layer(self, layer) -> None:
        if self.orders[layer]:
            self.order_mapping.pop(self.orders[layer].id, None)
            self.orders[layer] = None

    def get_layer_num(self, price: float) -> int:
        """
        Return layer number based on price.
        TODO: use binary search to increase efficiency
        TODO: implement short part
        """
        if price > self.grid_prices_long[0]:
            return 0

        for i in range(1, self.num_of_layers+1):
            if price > self.grid_prices_long[i]:
                return i

        return self.num_of_layers + 1

    def place_order(self, symbol: str, side: str, price: float, type: str, size: float) -> Order:
        """
        Wrapper place order method
        """
        try:
            response = self.place_order_cb(
                symbol=symbol,
                side=side,
                price=price,
                type=type,
                quantity=size)

            color = 'green' if side == 'buy' else 'red'
            logger.info('Successfully placed a %s order of %f %s at $%f.' % (side, size, symbol, price))

            return Order(response)
        except Exception as e:
            color = 'yellow'
            logger.info('Failed to place a %s order of %f %s at $%f due to: %s.' % (side, size, symbol, price, e))
            return None

    def place_buffer_orders(self, symbol: str, layer: int) -> List[int]:
        """
        Update orders
        """
        # Clean up order on currrent layer
        self._clean_up_order_with_layer(layer)

        for i in range(1, self.grid_buffer+1):
            sell_layer, buy_layer = layer - i, layer + i
            if sell_layer >= 0:
                if self.orders[sell_layer]:
                    if self.orders[sell_layer].status == OrderStatus.CLOSED:
                        self.order_mapping.pop(self.orders[sell_layer].id)
                        self.place_sell_order(sell_layer)

                else:
                    self.place_sell_order(sell_layer)
            if buy_layer <= self.num_of_layers:
                if self.orders[buy_layer]:
                    if self.orders[buy_layer].status == OrderStatus.CLOSED:
                        self.order_mapping.pop(self.orders[buy_layer].id)
                        self.place_buy_order(buy_layer)
                else:
                    self.place_buy_order(buy_layer)


    def place_sell_order(self, sell_layer):
        order = self.place_order(
            self.symbol,
            'sell',
            self.grid_prices_long[sell_layer],
            'limit',
            self.grid_volume)
        self.orders[sell_layer] = order
        if order:
            self.order_mapping.update({order.id: sell_layer})

    def place_buy_order(self, buy_layer):
        order = self.place_order(
            self.symbol,
            'buy',
            self.grid_prices_long[buy_layer],
            'limit',
            self.grid_volume)
        self.orders[buy_layer] = order
        if order:
            self.order_mapping.update({order.id: buy_layer})
