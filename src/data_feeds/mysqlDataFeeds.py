

import datetime
from sqlalchemy import create_engine


from backtrader.feed import DataBase
from backtrader import date2num
import backtrader as bt

class MySQLDataMarketA(DataBase):

    params = (
        ('host','localhost'),
        ('username','root'),
        ('password','123456'),
        ('db','road2rich2'),
        ('port','3306'),
        ('fromdate',datetime.datetime.min),
        ('todate',datetime.datetime.max),
        ('code',''),
        ('timeframe',bt.TimeFrame.Minutes)

    )

    lines = (
        'amount',
    )

    def __init__(self):
        super(MySQLDataMarketA, self).__init__()
        self.engine = create_engine(
            "mysql+pymysql://{username}:{passsword}@{host}:{port}/{database}?charset=utf8&use_unicode=1".format(
                username = self.p.username,
                passsword = self.p.password,
                host = self.p.host,
                port = self.p.port,
                database = self.p.db
            )
        )

    def start(self):
        self.conn = self.engine.connect()
        sql = "SELECT `time`,`open`,`close`,`high`,`low`,`volume`,`amount` FROM `TradingInfo` WHERE `code`='" + str(self.p.code) + "' AND `time` between '"+self.p.fromdate.strftime("%Y-%m-%d")+"' and '"+self.p.todate.strftime("%Y-%m-%d")+"' ORDER BY `time` ASC"
        self.result = self.conn.execute(sql)

    def stop(self):
        self.engine.dispose()

    def _load(self):
        '''
        这里每次都只加载一天的，所以要用fetch_one
        :return:
        '''
        one_row = self.result.fetchone()
        if one_row is None:
            return False


        self.lines.datetime[0] = date2num(one_row[0])
        self.lines.open[0] = float(one_row[1])
        self.lines.close[0] = float(one_row[2])
        self.lines.high[0] = float(one_row[3])
        self.lines.low[0] = float(one_row[4])
        self.lines.volume[0] = float(one_row[5])
        self.lines.amount[0] = float(one_row[6])
        self.lines.openinterest[0] = -1
        # print(self.lines.open[0])
        return True





if __name__ == '__main__':
    import json

    with open('../config.json','r') as f:
        config = json.load(f)

    mysqldata = MySQLDataMarketA(
        username = config['username'],
        password=config['password'],
        fromdate = datetime.datetime(2020,11,1),
        todate = datetime.datetime(2020,12,31),
        code = 'sh.600000'
    )

    mysqldata.start()







