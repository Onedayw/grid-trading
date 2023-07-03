import backtrader as bt
import sys
sys.path.append('.../')

from .long_grid_order_manager import LongGridOrderManager
from gateway.rest_client import RestClient
from logger.logger_config import logger


class LongGridStrategy(bt.Strategy):
    params = (
        ('symbol', 'BTC-USDT'),
        ('start_price', 25000),
        ('num_of_layers', 100),
        ('grid_buffer', 10),
        ('grid_interval', 0.01),
        ('grid_volume', 1),
    )

    def __init__(self) -> None:
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        
        self.order_manager = LongGridOrderManager(
            symbol=self.params.symbol,
            start_price=self.params.start_price,
            num_of_layers=self.params.num_of_layers,
            grid_buffer=self.params.grid_buffer,
            grid_interval=self.params.grid_interval,
            grid_volume=self.params.grid_volume,
            cb=self.place_order
            )
        
        # Place initail orders
        self.buy(price=self.dataclose[0], size=self.order_manager.grid_buffer*self.order_manager.grid_volume)


    def next(self) -> None:
        # Simply log the closing price of the series from the reference
        logger.info('Close, %.2f' % self.dataclose[0])

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                logger.info('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                logger.info('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)
            
            layer = self.order_manager.order_mapping.get(order.ref)
            self.order_manager.place_buffer_orders(self.params.symbol, layer)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.warning('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit',
                    reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    client_id: str = None, reject_after_ts: float = None) -> dict:
        if side == 'buy':
            order = self.buy(
                exectype=bt.Order.Limit,
                price=price,
                size=size
            )

            return order
        
        elif side == 'sell':
            order = self.sell(
                exectype=bt.Order.Limit,
                price=price,
                size=size
            )

            return order
        