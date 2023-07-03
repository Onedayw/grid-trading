import os
import sys
sys.path.append('..')

import argparse
import backtrader as bt
import datetime
import logging
import pandas as pd
import quantstats

from datetime import datetime, timedelta
from logger.logger_config import logger
from strategy.long_grid.long_gird_strategy import LongGridStrategy


def set_log_level():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()    
    logging.basicConfig(level=args.loglevel)

if __name__ == '__main__':
    set_log_level()

    cerebro = bt.Cerebro()
    
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    symbol_pair = 'LEVER-USDT'
    filename = symbol_pair + '.csv'
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../data/', filename)

    dataframe = pd.read_csv(datapath,
        index_col='open_time',
        parse_dates=['open_time'],
        date_parser=lambda x: datetime.utcfromtimestamp(int(x)/1000)
        )

    start_date, end_date = datetime.now() - timedelta(days=365), datetime.now()

    data = bt.feeds.PandasData(
        dataname=dataframe,
        fromdate=datetime.now() - timedelta(days=365),
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.addstrategy(
        LongGridStrategy,
        symbol=symbol_pair,
        start_price=0.0015,
        num_of_layers=100,
        grid_buffer=10,
        grid_interval=0.01,
        grid_volume=100000)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(commission=0.00014, leverage=3.0)

    logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    strat = results[0]
    portfolio_stats = strat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)

    # Generate a html page for stats
    # quantstats.reports.html(
    #     returns,
    #     output='stats.html',
    #     title='%s Grid Trading (%s - %s)' % (symbol_pair, start_date.date(), end_date.date()))

    # Generate an interactive graph
    cerebro.plot()