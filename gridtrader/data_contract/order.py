import datetime
import pandas
import time
from typing import Optional, Dict

from .enums import OrderType, OrderSide, OrderStatus


class Order:
    def __init__(self, id: int, market: str, type: str, side: str, price: float,
        size: float, filled_size: float, remaining_size: float,
        average_fill_size: float, status: str, created_at: str,
        reduce_only: bool, ioc: bool, post_only: bool, client_id: Optional[str]) -> None:
        self.id = id
        self.market = market
        self.type = OrderType[type]
        self.side = OrderSide[side]
        self.price = price
        self.size = size
        self.filled_size = filled_size
        self.remaining_size = remaining_size
        self.average_fill_size = average_fill_size
        self.status = OrderStatus[status]
        self.created_at = int(pandas.Timestamp(created_at).timestamp())
        self.reduce_only = reduce_only
        self.ioc = ioc
        self.post_only = post_only

    def __init__(self, data: Dict) -> None:
        self.id = data['id']
        self.market = data['market']
        self.type = OrderType[data['type'].upper()]
        self.side = OrderSide[data['side'].upper()]
        self.price = data['price']
        self.size = data['size']
        self.filled_size = data['filledSize']
        self.remaining_size = data['remainingSize']
        self.average_fill_size = data['avgFillPrice']
        self.status = OrderStatus[data['status'].upper()]
        self.created_at = int(pandas.Timestamp(data['createdAt']).timestamp())
        self.reduce_only = data['reduceOnly']
        self.ioc = data['ioc']
        self.post_only = data['postOnly']

    # def __getitem__(self, key):
    #     return self._vet[key]
