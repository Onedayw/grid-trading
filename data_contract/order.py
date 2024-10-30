import backtrader as bt
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict
from sqlalchemy import create_engine, Column, String, Float, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base

from .enums import OrderType, OrderSide, OrderStatus


Base = declarative_base()

@dataclass
class BinanceSpotOrder(Base):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str               # Binance order id (orderId)
    market: str                 # Coin pair (symbol)
    type: OrderType             # Market or Limit (type)
    side: OrderSide             # Buy or Sell (side)
    price: float                # Order price (price)
    size: float                 # Original quantity (origQty)
    filled_size: float          # Executed quantity (executedQty)
    status: OrderStatus         # Order status (status)
    created_at: int             # Transaction time (transacTime)
    client_id: Optional[str]    # User defined order id (clientOrderId)

    @staticmethod
    def from_dict(data: Dict) -> 'BinanceSpotOrder':
        return BinanceSpotOrder(
            id=data.get('id', str(uuid.uuid4())),
            order_id=data['orderId'],
            market=data['symbol'],
            type=OrderType[data['type'].upper()],
            side=OrderSide[data['side'].upper()],
            price=float(data['price']),
            size=float(data['origQty']),
            filled_size=float(data['executedQty']),
            status=OrderStatus[data['status'].upper()],
            created_at=data['transacTime'],
            client_id=data.get('clientOrderId'),
        )

    def from_data(self, data: bt.OrderBase) -> 'BinanceSpotOrder':
        return BinanceSpotOrder(
            id=data.ref,
            order_id=data.ref,
            market='BT',
            type=OrderType.LIMIT if data.exectype == bt.Order.Limit else OrderType.MARKET,
            side=OrderSide.BUY if data.isbuy() else OrderSide.SELL,
            price=data.price,
            size=data.size,
            filled_size=data.size,
            status=OrderStatus.NEW,
            created_at=0,
            client_id=None
        )
