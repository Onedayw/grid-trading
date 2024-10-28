from enum import Enum

class OrderType(Enum):
    LIMIT = 0
    MARKET = 1

class OrderSide(Enum):
    BUY = 0
    SELL = 1

class OrderStatus(Enum):
    NEW = 0
    OPEN = 1
    CLOSED = 2

class Platform(Enum):
    FTX = 0
    BINANCE_SPOT = 1
    BINANCE_FUTURES = 2
    BINANCE_PROFOLIO = 3