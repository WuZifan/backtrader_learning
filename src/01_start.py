
import backtrader as bt
import os
import sys
import datetime


class TestStrategy(bt.Strategy):

    params = (
        # ('exitbars',5),
        ('maperiod',5),
    )

    def log(self,txt,dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' %(dt.isoformat(),txt))
    

    def __init__(self):
        # TODO:Question1: whats inside self.datas
        self.dataclose = self.datas[0].close

        self.order = None

        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0],period = self.params.maperiod)
        bt.indicators.SimpleMovingAverage(self.datas[0], period=5)

        bt.indicators.ExponentialMovingAverage(self.datas[0],period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0],period=25,subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi,period=10)
        bt.indicators.ATR(self.datas[0],plot=False)


    def notify_order(self,order):
        print(order.status)

        # 订单处于提交状态或者接受状态时，什么都不做
        if order.status in [order.Submitted,order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('已买入， %.2f'%order.executed.price)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('已卖出， %.2f'%order.executed.price)
            
            self.bar_executed = len(self)
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('订单失败')
        
        self.order = None
    

    def notify_trade(self,trade):
        # 一买一卖算交易
        if not trade.isclosed:
            return
        self.log('交易利润，毛利润 %.2f, 净利润 %.2f' %(trade.pnl,trade.pnlcomm))

    def next(self):
        self.log('Close %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            # Note: 下标是0表示今天，-1表示昨天，-2表示前天
            # if self.dataclose[0]<self.dataclose[-1]:
            #     if self.dataclose[-1]<self.dataclose[-2]:
            #         self.log('买入, %.2f' % self.dataclose[0])
            #         self.order = self.buy()

            if self.dataclose[0] > self.sma[0]:
                self.log('买入, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:
            # if len(self)>=(self.bar_executed+self.params.exitbars):
            if self.dataclose[0]<self.sma[0]:
                self.log('卖出, %.2f'%self.dataclose[0])
                self.order = self.sell()

if __name__=='__main__':
    cerebro = bt.Cerebro()


    # 1.add data
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    print(modpath)


    datapath = os.path.join(modpath,'../data/orcl-1995-2014.txt')
    mydata = bt.feeds.YahooFinanceCSVData(dataname=datapath,
                    fromdate = datetime.datetime(2012,12,1),
                    todate = datetime.datetime(2014,12,31),
                    reverse = False)
    cerebro.adddata(mydata)

    # 2.set strategy
    cerebro.addstrategy(TestStrategy)

    # 3. set init money
    cerebro.broker.set_cash(100000)

    cerebro.addsizer(bt.sizers.FixedSize,stake = 10)
    # Note: 原始默认每次只买一股，这里指定每次买多少股
    cerebro.broker.setcommission(commission=0.001)
    print(cerebro.broker.getvalue())
    cerebro.run()

    print(cerebro.broker.getvalue())

    # cerebro.plot()
