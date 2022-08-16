import sys
import time
sys.path.append('../')

from functools import reduce
from gateway.ftx.websocket_client import FtxWebsocketClient
from gateway.ftx.rest_client import FtxRestClient
from termcolor import colored


class GridTrader:
    def __init__(self, start_price=0, grid_amount=0, grid_interval=0.005, grid_volume=0, api_key=None, api_secret=None) -> None:
        self._start_price = start_price
        self._grid_amount = grid_amount
        self._grid_interval = grid_interval
        self._grid_volume = grid_volume

        self.grid_region_long = [self._grid_interval] * self._grid_amount  # price intervals for long (grid density)
        self.grid_region_short = [self._grid_interval] * self._grid_amount  # price intervals for short (grid density)
        self.grid_volumes_long = [i * self._grid_volume for i in range(self._grid_amount + 1)]  # trade volumes for long
        self.grid_volumes_short = [i * self._grid_volume for i in range(self._grid_amount + 1)]  # trade volumes for short
        self.grid_prices_long = [reduce(lambda p, r: p*(1-r), self.grid_region_long[:i], self._start_price) for i in range(self._grid_amount + 1)]  # gride prices for long
        self.grid_prices_short = [reduce(lambda p, r: p*(1+r), self.grid_region_short[:i], self._start_price) for i in range(self._grid_amount + 1)]  # gride prices for short

        self.websocket_client = FtxWebsocketClient(api_key, api_secret)
        self.websocket_client.connect()
        self._update_last_bid()
        self.rest_client = FtxRestClient(api_key, api_secret)

        print("Grid trading starts, start price: %f, trade volumes for long:%s, grid prices for long:%s, grid prices for short:%s" % (
            self._start_price,
            self.grid_volumes_long,
            self.grid_prices_long,
            self.grid_prices_short))

    def _update_last_bid(self) -> float:
        self.orderbook = self.websocket_client.get_orderbook(market="ETH/USDT")
        self.last_bid_price = self.orderbook['bids'][0][0]
        self.last_bid_volume = self.orderbook['bids'][0][1]
        return self.last_bid_price

    def _place_order(self, rest_client, market, side, price, type, size) -> int:
        response = rest_client.place_order(
            market=market,
            side=side,
            price=price,
            type=type,
            size=size)

        color = 'green' if side == 'buy' else 'red'
        print(colored('Successfully placed a %s order of %f ETH at $%f.' % (side, size, price), color))

        return response['id']

    def wait_price(self, layer) -> None:
        """
        等待行情最新价变动到其他档位,则进入下一档位或回退到上一档位
        如果从下一档位回退到当前档位,则设置为当前对应的持仓手数
        layer: 当前所在第几个档位层次; layer>0 表示多头方向, layer<0 表示空头方向
        """
        if layer > 0 or self.last_bid_price <= self.grid_prices_long[0]:  # long
            while True:
                self._update_last_bid()
                # 如果当前档位小于最大档位,并且最新价小于等于下一个档位的价格: 则设置为下一档位对应的手数后进入下一档位层次
                if layer < self._grid_amount and self.last_bid_price <= self.grid_prices_long[layer + 1]:
                    order_id = self._place_order(self.rest_client, 'ETH/USDT', 'buy', self.last_bid_price, 'limit', self.grid_volumes_long[layer+1])
                    print(colored('最新价: %f, 进入: 多头第 %d 档' % (self.last_bid_price, layer + 1), 'yellow'))
                    self.wait_price(layer + 1)
                    # 从下一档位回退到当前档位后, 设置回当前对应的持仓手数
                    order_id = self._place_order(self.rest_client, 'ETH/USDT', 'sell', self.last_bid_price, 'limit', self.grid_volumes_long[layer+1])
                # 如果最新价大于当前档位的价格: 则回退到上一档位
                if self.last_bid_price > self.grid_prices_long[layer]:
                    print(colored('最新价: %f, 回退到: 多头第 %d 档' % (self.last_bid_price, layer), 'yellow'))
                    return
                time.sleep(1)
