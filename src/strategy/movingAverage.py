import backtrader as bt


class LineCrossStrategy(bt.Strategy):
    params = (
        ('maperiod', 5),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.sma5 = bt.indicators.MovingAverageSimple(self.datas[0], period=5)
        self.sma20 = bt.indicators.MovingAverageSimple(self.datas[0], period=20)
        self.sma60 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.p.maperiod)

        self.crossOver5and60 = bt.indicators.CrossOver(self.sma5, self.sma60, plot=False)
        self.crossOverCloseand20 = bt.indicators.CrossOver(self.dataclose, self.sma20, plot=False)

        self.buyPrice = None
        self.order = None
        self.maxProfitPercentage = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyPrice = order.executed.price
                self.log('已买入， %.2f' % order.executed.price)
            elif order.issell():
                self.log('已卖出， %.2f' % order.executed.price)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Fail')

        self.order = None

    def notify_trade(self, trade):
        # 一买一卖算交易
        if not trade.isclosed:
            return
        self.log('交易利润，毛利润 %.2f, 净利润 %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # self.log('Close %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            # 未持仓，看是否有买入信号
            # if self.sma5[0]>self.sma60[0]:
            #     if self.sma5[-1]<self.sma60[-1]:
            if self.crossOver5and60[0] == 1:
                self.log('买入, %.2f' % self.dataclose[0])

                # 这里可以用allInSizer来代替
                # cash = self.broker.get_cash()
                # buy_size = int(cash/(100*self.dataclose[0]))*100

                self.log('Cash %.2f' % (self.broker.get_cash()))

                self.order = self.buy()

        else:
            # 持仓，看是否有卖出信号
            if self.shouldSell():
                self.log('卖出, %.2f' % self.dataclose[0])

                # self.order = self.sell()
                # 清仓可以用close
                self.buyPrice = None
                self.order = self.close()

    def shouldSell(self):
        '''
        严格来说，卖点也属于一种止损，可以理解为是技术面的止损
        :return:
        '''
        if self.dataclose[0] > self.buyPrice:
            # 止盈
            return self.sellWhenProfit()
        else:
            # 止损
            return self.sellWhenLoss()

    def sellWhenLoss(self):
        # 止损方式1：下跌达到某个幅度就止损：
        if (self.buyPrice - self.dataclose[0]) / self.buyPrice >= 0.05:
            return True

    def sellWhenProfit(self):
        # 1、计算盈利回撤
        profit_percentage = (self.dataclose[0] - self.buyPrice) / self.buyPrice
        if profit_percentage > self.maxProfitPercentage:
            self.maxProfitPercentage = profit_percentage

        max_return = 2 * 0.1 * self.maxProfitPercentage + 0.01
        if self.maxProfitPercentage > 0.1 and profit_percentage <= (self.maxProfitPercentage - max_return):
            self.log("卖出，最大收益率为 %.2f，此时收益率为%.2f" % (self.maxProfitPercentage, profit_percentage))
            return True

        # 这里可以用crossOver indicator来代替
        # 技术面止盈1：ma5下穿过ma60
        if self.crossOver5and60[0] == -1:
            self.log('卖出，5日线下穿60日线')
            return True

        # 技术面止盈2：日线下穿ma20
        if self.crossOverCloseand20[0] == -1:
            self.log(txt='卖出，日线下穿20日均线')
            return True
