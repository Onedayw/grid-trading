import sys
sys.path.append('.../')

from functools import reduce
from typing import List
from termcolor import colored

from data_contract.order import Order
from data_contract.enums import OrderStatus
from gateway.ftx.rest_client import FtxRestClient


class NeutralGridOrderManager:
    def __init__(self, start_price: float, num_of_layers: int, grid_buffer: int,
        grid_interval: float, grid_volume: float, client: FtxRestClient) -> None:
        self.start_price = start_price
        self.num_of_layers = num_of_layers
        self.grid_buffer = grid_buffer
        self.grid_interval = grid_interval
        self.grid_volume = grid_volume
        self.client = client

        self.grid_region_long = [self.grid_interval] * self.num_of_layers  # price intervals for long (grid density)
        self.grid_region_short = [self.grid_interval] * self.num_of_layers  # price intervals for short (grid density)
        self.grid_volumes_long = [i * self.grid_volume for i in range(self.num_of_layers + 1)]  # trade volumes for long
        self.grid_volumes_short = [i * self.grid_volume for i in range(self.num_of_layers + 1)]  # trade volumes for short
        self.grid_prices_long = [reduce(lambda p, r: p*(1-r), self.grid_region_long[:i], self.start_price) for i in range(self.num_of_layers + 1)]  # gride prices for long
        self.grid_prices_short = [reduce(lambda p, r: p*(1+r), self.grid_region_short[:i], self.start_price) for i in range(self.num_of_layers + 1)]  # gride prices for short

        self.last_filled_order = None
        self._init_orders(client)
        print('Order mapping: ' + str(self.order_mapping))

    def _init_orders(self, client: FtxRestClient) -> None:
        """
        Place initial limit orders
        """
        self.orders = [None] * (self.num_of_layers + 1)
        self.order_mapping = {}
        grid_num = self.get_layer_num(self.start_price)

        # Place sell orders
        for i in range(1, self.grid_buffer+1):
            if grid_num - i < 0:
                break
            else:
                order = self.place_order(client, 'ETH/USDT', 'sell', self.grid_prices_long[grid_num-i], 'limit', self.grid_volume)
                self.orders[grid_num-i] = order
                if order:
                    self.order_mapping.update({order.id: grid_num-i})

        # Place buy OrderSide
        for i in range(self.grid_buffer):
            if grid_num + i > self.num_of_layers:
                break
            else:
                order = self.place_order(client, 'ETH/USDT', 'buy', self.grid_prices_long[grid_num+i], 'limit', self.grid_volume)
                self.orders[grid_num + i] = order
                if order:
                    self.order_mapping.update({order.id: grid_num+i})

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

    def place_order(self, client: FtxRestClient, market: str, side: str, price: float, type: str, size: float) -> Order:
        try:
            response = client.place_order(
                market=market,
                side=side,
                price=price,
                type=type,
                size=size)

            color = 'green' if side == 'buy' else 'red'
            print(colored('Successfully placed a %s order of %f ETH at $%f.' % (side, size, price), color))

            return Order(response)
        except Exception as e:
            color = 'yellow'
            print(colored('Failed to place a %s order of %f ETH at $%f due to: %s.' % (side, size, price, e)), color)
            return None

    def place_buffer_orders(self, layer: int) -> List[int]:
        """
        Update orders
        """
        # Clean up order on currrent layer
        self._clean_up_order_with_layer(layer)

        for i in range(1, self.grid_buffer+1):
            print('layer is %d' % layer)
            print(self.orders)
            if layer - i >= 0:
                if self.orders[layer-i]:
                    if self.orders[layer-i].status == OrderStatus.CLOSED:
                        self.order_mapping.pop(self.orders[layer-i].id)
                        order = self.place_order(self.client, 'ETH/USDT', 'sell', self.grid_prices_long[layer-i], 'limit', self.grid_volume)
                        self.orders[layer-i] = order
                        if order:
                            self.order_mapping.update({order.id: layer-i})
                else:
                    order = self.place_order(self.client, 'ETH/USDT', 'sell', self.grid_prices_long[layer-i], 'limit', self.grid_volume)
                    self.orders[layer-i] = order
                    if order:
                        self.order_mapping.update({order.id: layer-i})
            if layer + i <= self.num_of_layers:
                if self.orders[layer+i]:
                    if self.orders[layer+i].status == OrderStatus.CLOSED:
                        self.order_mapping.pop(self.orders[layer+i].id)
                        order = self.place_order(self.client, 'ETH/USDT', 'buy', self.grid_prices_long[layer+i], 'limit', self.grid_volume)
                        self.orders[layer+i] = order
                        if order:
                            self.order_mapping.update({order.id: layer+i})
                else:
                    order = self.place_order(self.client, 'ETH/USDT', 'buy', self.grid_prices_long[layer+i], 'limit', self.grid_volume)
                    self.orders[layer+i] = order
                    if order:
                        self.order_mapping.update({order.id: layer+i})
