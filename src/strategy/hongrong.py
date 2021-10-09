
import backtrader as bt


class HongRong333_1(bt.Strategy):
    """
    - 空仓时，如果股价小于前7天高点P1%，那么买入1/3
    - 建仓后，如果股价小于前7天高点P2%，那么买入1/3
    - 2/3仓后，如果股价大于前7天低点P3%，那么卖出1/3

    Args:
        bt ([type]): [description]

    Returns:
        [type]: [description]
    """
    params={
        ('buildPercentage',0.03),
        ('rollInPercentage',0.05),
        ('rollOutPercentage',0.10),
    }

        # states defination
    Empty, Build, RollIn,RollOut = range(4)
    status = [
        'Empty', 'Build', 'RollIn','RollOut'
    ]

    def log(self,txt,dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' %(dt.isoformat(),txt))
    

    def __init__(self) -> None:
        super(HongRong333_1,self).__init__()

        self.close = self.datas[0].close
        self.week_max = bt.talib.MAX(self.datas[0],timeperiod=7,plot=True)
        self.week_min = bt.talib.MIN(self.datas[0],timeperiod=7,plot=True)
        self.weekly_high = self.datas[1].high

        self.order = None

        self.status = self.Empty
        self.status_map = {
            self.Empty:self._build_position,
            self.Build:self._rollIn,
            self.RollIn:self._rollOut,
            self.RollOut:self._rollIn,
        }

    def notify_order(self, order):
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

        # return super().notify_order(order)

    def next(self):
        if self.order:
            return
        self.order = self.status_map[self.status]()

    def _build_position(self):
        if self.close[0]<self.week_max[0]:
            percentage = (self.week_max[0]-self.close[0])/self.week_max[0]
            if percentage>=self.params.buildPercentage:
                self.status = self.Build
                price = self.close[0]
                cash = self.broker.get_cash()
                share = int(cash/3/(100*price))*100
                return self.buy(size=share)

    def _rollIn(self):
        if self.close[0]<self.week_max[0]:
            percentage = (self.week_max[0]-self.close[0])/self.week_max[0]
            if percentage>=self.params.rollInPercentage:
                self.status=self.RollIn
                price = self.close[0]
                cash = self.broker.get_cash()
                share = int(cash/2/(100*price))*100
                return self.buy(size=share)

    def _rollOut(self):
        if self.close[0]>self.week_min[0]:
            percentage = (self.close[0]-self.week_min[0])/self.week_min[0]
            if percentage>=self.params.rollOutPercentage:
                self.status=self.RollOut
                share = int(self.broker.get_fundshares()/2/100)*100
                return self.sell(size=share)


class HongRong333_2(bt.Strategy):
    params={
        ('buildPercentage',0.03),
        ('rollInPercentage',0.05),
        ('rollOutPercentage',0.10),
    }

        # states defination
    Empty, Build, RollIn,RollOut = range(4)
    STATUS = [
        'Empty', 'Build', 'RollIn','RollOut'
    ]

    def log(self,txt,dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s, hahaha' %(dt.isoformat(),txt))
    

    def __init__(self) -> None:
        print("init %s"%self.__class__)
        super(HongRong333_2,self).__init__()

        self.daily_close = self.datas[0].close

        self.week_max = bt.talib.MAX(self.datas[0],timeperiod=5,plot=True)
        self.week_min = bt.talib.MIN(self.datas[0],timeperiod=5,plot=True)
        self.weekly_high = self.datas[1].high
        self.weekly_low = self.datas[1].low
        self.order = None

        self.status = self.Empty
        self.status_map = {
            self.Empty:self._build_position,
            self.Build:self._rollIn,
            self.RollIn:self._rollOut,
            self.RollOut:self._rollIn,
        }

    def notify_trade(self,trade):
        # 一买一卖算交易
        if not trade.isclosed:
            return
        self.log('交易利润，毛利润 %.2f, 净利润 %.2f' %(trade.pnl,trade.pnlcomm))


    def notify_order(self, order):
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

        # return super().notify_order(order)

    def next(self):
        print(self.datas[0].datetime.date(),self.daily_close[0],self.weekly_high[0])
        if self.order:
            return
        # print(self.status,self.STATUS[self.status])
        self.order = self.status_map[self.status]()

    def _build_position(self):
        if self.daily_close[0]<self.week_max[0]:
            percentage = (self.week_max[0]-self.daily_close[0])/self.week_max[0]
            if percentage>=self.params.buildPercentage:
                self.status = self.Build
                price = self.daily_close[0]
                cash = self.broker.get_cash()
                share = int(cash/3/(100*price))*100
                return self.buy(size=share)

    def _rollIn(self):
        """买入策略
        采用周滚动：
            当周每个交易日与前一周的收盘价相比：
                前一周收盘价高于前两周收盘价；
                并且当周交易日低于前一周收盘价；
                那么比较跌幅，如果跌幅达到一定水平，执行买入


        Returns:
            : [description]
        """
        if len(self.weekly_high)>=2:
            if self.weekly_high[-1]>self.weekly_high[-2]:
                if self.daily_close[0]<self.weekly_high[-1]:
                    percentage = (self.weekly_high[-1]-self.daily_close[0])/self.weekly_high[-1]
                    if percentage>=self.params.rollInPercentage:
                        self.status = self.RollIn
                        price = self.daily_close[0]
                        cash = self.broker.get_cash()
                        share = int(cash/3/(100*price))*100
                        return self.buy(size=share)
        
    def _rollOut(self):
        if len(self.weekly_high)>=2:
            if self.weekly_high[-1]<self.weekly_high[-2]:
                if self.daily_close[0]>self.weekly_high[-1]:
                    percentage = (self.daily_close[0]-self.weekly_high[-1])/self.weekly_high[-1]
                    if percentage>=self.params.rollOutPercentage:
                        self.status = self.RollOut
                        share = int(self.broker.get_fundshares()/2/100)*100
                        return self.sell(size=share)


