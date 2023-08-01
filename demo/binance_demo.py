import time
import sys
sys.path.append('../')

from strategy.long_grid.long_grid_trading import LongGridTrader
from strategy.neutral_grid.neutral_grid_trading import NeutralGridTrader

if __name__ == '__main__':
    api_key = ''
    api_secret = ''

    gt = LongGridTrader(
        symbol='ETHUSDT',
        start_price=1850,
        num_of_grids=20,
        grid_interval=0.01,
        grid_volume=0.005,
        api_key=api_key,
        api_secret=api_secret)
    #gt.run(number_of_layers=3)
