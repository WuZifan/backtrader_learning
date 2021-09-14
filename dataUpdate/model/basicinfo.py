from dataUpdate import Base
from sqlalchemy import Column, Integer, String,Float,DateTime,Boolean



'''
    1、股票基础信息
'''
class StockBasic(Base):
    __tablename__='stock_basic'
    __table_args__ = {'extend_existing': True}

    # ts_code = Column(String(100),primary_key=True)
    code = Column(String(100),primary_key=True)
    symbol = Column(String(100))
    name = Column(String(100))
    area = Column(String(100))
    industry = Column(String(100))
    market = Column(String(100))
    list_date = Column(String(100))
    circulating_market_cap = Column(Float)
    sw_l1 = Column(String(100))
    sw_l3 = Column(String(100))
    circulating_cap = Column(Float)
    start_time = Column(DateTime,index=True)
    end_time = Column(DateTime,index=True)


    # test_id = Column(Integer)

    def __init__(self,ts_code,symbol,name,area,industry,market,list_date,
                 sw_l1,sw_l3,circulating_market_cap,circulating_cap):
        self.code = ts_code
        self.symbol = symbol
        self.name = name
        self.area = area
        self.industry = industry
        self.market = market
        self.list_date = list_date
        self.sw_l1 = sw_l1
        self.sw_l3 = sw_l3
        self.circulating_market_cap = circulating_market_cap
        self.circulating_cap = circulating_cap


    def __repr__(self):
        return "{},{}".format(self.code,self.symbol, self.name,self.area,self.industry)


class StockEarningReport(Base):
    '''
    1、中英对照表
      "序号":"id",
      "股票代码":"code",
      "股票简称":"name",
      "每股收益":"earning_per_share",
      "营业收入-营业收入":"revenue",
      "营业收入-同比增长":"revenue_yoy_rise",
      "营业收入-季度环比增长":"revenue_sos_rise",
      "净利润-净利润":"net_profit",
      "净利润-同比增长":"net_profit_yoy_rise",
      "净利润-季度环比增长":"net_profit_sos_rise",
      "每股净资产":"net_asset_value_per_share",
      "净资产收益率":"return_on_equity",
      "每股经营现金流量":"operating_cash_flow_per_share",
      "销售毛利率":"gross_profit_ratio",
      "所处行业":"industry",
      "最新公告日期":"time"
    2、年收入怎么看：
        每年四份业绩报告：
            0331：一季报
            0630：半年报
            0931：三季报
            1231：年报
        所以只需要看每一年的最后一份报告即可
    '''
    __tablename__ = 'stock_earning_report'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer,primary_key=True)
    code = Column(String(100),index=True)
    earning_per_share = Column(Float)
    revenue = Column(Float)
    revenue_yoy_rise = Column(Float)
    revenue_sos_rise = Column(Float)
    net_profit = Column(Float)
    net_profit_yoy_rise = Column(Float)
    net_profit_sos_rise = Column(Float)
    return_on_equity = Column(Float)
    operating_cash_flow_per_share = Column(Float)
    gross_profit_ratio = Column(Float)
    year = Column(Integer)
    date = Column(String(10))
    # time = Column(DateTime,index=True)

    def __init__(self):
        pass

    def __repr__(self):
        return "{},{},{}".format(self.code,self.earning_per_share,self.year)




if __name__ == '__main__':
    from sqlalchemy.orm import Session
    from dataUpdate import engine

    session = Session(engine)

    all_stocks = session.query(StockEarningReport).all()
    for stk in all_stocks:
        print(stk,type(stk))
        break

