import datetime
import pandas as pd
import baostock as bs
from dataUpdate import logger

def login_bs():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    logger.info('login respond  error_msg:'+lg.error_msg)


def getStockHistoryInfo(stock_code:str,start_date='2017-9-25',end_date='2017-10-29',frequency='30'):
    '''
    :param stock_code:
    :param start_date:
    :param end_date:
    :param frequency: tickle维度，默认30分钟级别
    :return:
    '''
    rs = bs.query_history_k_data_plus(stock_code,
    "date,time,code,open,high,low,close,volume,amount,adjustflag",
    start_date, end_date,
    frequency=frequency, adjustflag="3")

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    if len(result)==0:
        return result
    result['time'] = result['time'].map(timeConvert)
    result = result[['code','time','open','close','high','low','volume','amount']]
    return result

def timeConvert(x):
    '''
    将 20050104100000000 格式的时间，转换成 2005-02-24 10:00:00格式
    :param x:
    :return:
    '''
    x = str(x)
    temp_time = x[:-3]
    temp_time = datetime.datetime.strptime(temp_time, '%Y%m%d%H%M%S')
    return temp_time

# login_bs()