import sys
sys.path.append('.../')

import pandas
from data_contract.order import Order
from data_contract.enums import OrderSide


class StatManager:
    def __init__(self, start_balance: float):
        self._start_balance = start_balance
        self._closed_orders = []
        self._placed_orders = []
        self._grid_orders = []
        self._grid_profit = 0.0
        self._volume = 0.0

    def add_closed_order(self, order: Order):
        self._closed_orders.append(order)
        self._volume += order.size * order.price
        print(order)

        if not self._grid_orders or order.side == self._grid_orders[-1].side:
            self._grid_orders.append(order)
        else:
            prev_order = self._grid_orders.pop()
            self._grid_profit += abs(order.price - prev_order.price) * order.size

    def get_grid_profit(self) -> float:
        return self._grid_profit

    def get_total_profit(self, current_balance: float) -> float:
        return current_balance - self._start_balance

    def get_volume(self) -> float:
        return self._volume
