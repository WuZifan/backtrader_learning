
import backtrader as bt
import os
import sys
import datetime
import pandas as pd
import json
from strategy.movingAverage import LineCrossStrategy
from strategy.hongrong import HongRong333
from data_feeds.mysqlDataFeeds import MySQLDataMarketA


if __name__=='__main__':
    cerebro = bt.Cerebro()


    # 1.add data
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # print(modpath)
    # datapath = os.path.join(modpath,'../data/orcl-1995-2014.txt')
    # mydata = bt.feeds.YahooFinanceCSVData(dataname=datapath,
    #                 fromdate = datetime.datetime(2012,12,1),
    #                 todate = datetime.datetime(2014,12,31),
    #                 reverse = False)

    with open('../config.json','r') as f:
        config = json.load(f)
    mydata = MySQLDataMarketA(
        username=config['username'],
        password=config['password'],
        fromdate=datetime.datetime(2018, 12, 31),
        todate=datetime.datetime(2019, 12, 31),
        code='sh.600031',
    )
    # cerebro.adddata(mydata)
    cerebro.resampledata(mydata,timeframe=bt.TimeFrame.Days)

    # 2.set strategy
    # cerebro.addstrategy(LineCrossStrategy,maperiod=60)
    # cerebro.optstrategy(LineCrossStrategy,maperiod=[30,60])
    cerebro.addstrategy(HongRong333)


    # 3. set init money
    cerebro.broker.set_cash(100000)

    # Note: 原始默认每次只买一股，这里指定每次买多少股
    # cerebro.addsizer(bt.sizers.FixedSize,stake = 10)
    cerebro.addsizer(bt.sizers.AllInSizerInt, percents=99)

    cerebro.broker.setcommission(commission=0.001)
    print(cerebro.broker.getvalue())

    # 添加analysis
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    # cerebro.addanalyzer(bt.analyzers.TimeDrawDown)
    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
    # cerebro.addanalyzer(bt.analyzers.SQN)

    cerebro.run()

    # print(thestrats)
    #
    # for thestrat in thestrats:
    # # thestrat = thestrats[0]
    #     print('Annual Return:', thestrat[0].analyzers[0].get_analysis())
    #     print('TimeDrawDown:', thestrat[0].analyzers[1].get_analysis())
    #     print('TradeAnalyzer:', thestrat[0].analyzers[2].get_analysis())
    #     print('SQN:', thestrat[0].analyzers[3].get_analysis())
    #
    #     print("")

    print(cerebro.broker.getvalue())

    cerebro.plot(
        style='line',
        barup='red',
        bardown='green'
    )



