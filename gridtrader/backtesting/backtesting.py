import argparse
import backtrader as bt
import datetime
import os.path
import pandas as pd
import quantstats
import sys
sys.path.append('../')

from datetime import datetime, timedelta
from strategy.long_grid.long_gird_strategy import LongGridStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(LongGridStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../data/ETH-USDT.csv')

    dataframe = pd.read_csv(datapath,
        index_col='open_time',
        parse_dates=['open_time'],
        date_parser=lambda x: datetime.utcfromtimestamp(int(x)/1000)
        )

    data = bt.feeds.PandasData(
        dataname=dataframe,
        fromdate=datetime.now() - timedelta(days=365),
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

    cerebro.broker.set_cash(1000000)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    strat = results[0]
    portfolio_stats = strat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)

    quantstats.reports.html(returns, output='stats.html', title='BTC Sentiment')
    cerebro.plot()