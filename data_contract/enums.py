from enum import Enum

class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    NEW = 0
    OPEN = 1
    CLOSED = 2

class Platform(Enum):
    FTX = 0
    BINANCE_SPOT = 1
    BINANCE_FUTURES = 2
    BINANCE_PROFOLIO = 3