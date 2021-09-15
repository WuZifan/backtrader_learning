
import backtrader as bt


class HongRong333(bt.Strategy):
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
        super().__init__()

        self.close = self.datas[0].close
        self.week_max = bt.talib.MAX(self.datas[0],timeperiod=7,plot=True)
        self.week_min = bt.talib.MIN(self.datas[0],timeperiod=7,plot=True)
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


        

        

