import argparse
from itertools import compress
import json
import datetime
import backtrader as bt
from backtrader.dataseries import TimeFrame
from strategy.hongrong import HongRong333_2,HongRong333_1
from data_feeds.mysqlDataFeeds import MySQLDataMarketA


class St0(bt.Strategy):
    def __init__(self):
        pass
    
    def next(self):
        print('st0 next', not self.position)

        if not self.position:
            self.buy()
        else:
            self.close()

    

class St1(bt.Strategy):
    def __init__(self):
        pass
    
    def next(self):
        print('st1 next', not self.position)
        if not self.position:
            self.buy()
        else:
            self.close()



class StFetcher(object):
    _STRATS = [St0,St1]

    def __new__(cls, *args, **kwargs):
        idx = kwargs.pop('idx')

        obj = cls._STRATS[idx](*args, **kwargs)

        print(obj.__class__)
        return obj


def runstrat(pargs=None):
    args = parse_args(pargs)

    cerebro = bt.Cerebro()
    with open('../config.json','r') as f:
        config = json.load(f)
    data =  MySQLDataMarketA(
        username=config['username'],
        password=config['password'],
        fromdate=datetime.datetime(2020, 12, 1),
        todate=datetime.datetime(2020, 12, 31),
        code='sh.600031',
    )
    # print(args.data)
    # data = bt.feeds.BacktraderCSVData(dataname=args.data)

    cerebro.adddata(data)
    # cerebro.resampledata(data,compression=8)
    # cerebro.resampledata(data,timeframe=bt.TimeFrame.Weeks)


    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.optstrategy(StFetcher, idx=[0,1])
    results = cerebro.run(maxcpus=1)

    strats = [x[0] for x in results]  # flatten the result
    for i, strat in enumerate(strats):
        rets = strat.analyzers.returns.get_analysis()
        print('Strat {} Name {}:\n  - analyzer: {}\n'.format(
            i, strat.__class__.__name__, rets))


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for strategy selection')

    parser.add_argument('--data', required=False,
                        default='../data/orcl-1995-2014_short.txt',
                        help='Data to be read in')

    parser.add_argument('--maxcpus', required=False, action='store',
                        default=None, type=int,
                        help='Limit the numer of CPUs to use')

    parser.add_argument('--optreturn', required=False, action='store_true',
                        help='Return reduced/mocked strategy object')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()