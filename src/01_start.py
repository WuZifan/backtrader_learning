
import backtrader as bt
import os
import sys
import datetime
import pandas as pd
import json
from strategy.movingAverage import LineCrossStrategy
from strategy.hongrong import HongRong333_1,HongRong333_2
from data_feeds.mysqlDataFeeds import MySQLDataMarketA

class CombineStrategy(object):
    _STRATS = [HongRong333_1, HongRong333_2]

    def __new__(cls, *args, **kwargs):
        idx = kwargs.pop('idx')
        print('idx',idx)

        obj = cls._STRATS[idx](*args, **kwargs)
        return obj


if __name__=='__main__':
    cerebro = bt.Cerebro()

    with open('../config.json','r') as f:
        config = json.load(f)
    mydata = MySQLDataMarketA(
        username=config['username'],
        password=config['password'],
        fromdate=datetime.datetime(2020, 1, 1),
        todate=datetime.datetime(2020, 12, 31),
        code='sh.600031',
    )
    # cerebro.adddata(mydata)
    cerebro.resampledata(mydata,timeframe=bt.TimeFrame.Days)
    cerebro.resampledata(mydata,timeframe=bt.TimeFrame.Weeks)
    cerebro.addanalyzer(bt.analyzers.Returns)

    cerebro.addstrategy(HongRong333_1)

    # 3. set init money
    cerebro.broker.set_cash(100000)

    cerebro.broker.setcommission(commission=0.001)

    # cerebro.optstrategy(CombineStrategy, idx=[0, 1])
    print(cerebro.broker.get_value())
    result = cerebro.run(maxcpus=1)
    print(cerebro.broker.get_value())
    print(cerebro.broker.get_cash())
    print(cerebro.broker.get_fundshares())

    print(result[0].analyzers.returns.get_analysis())
    # cerebro.plot(
    #     style='candle',
    #     barup='red',
    #     bardown='green'
    # )




    



