import tushare as ts

token = 'e554b98ac431b1146b1db6bcb89dde62837fd87fb4c31aca54ff249f'

pro = ts.pro_api(token=token)


def getStockBasicInfo():
    '''
    获取stock的基础信息
    :return:
    '''
    data = pro.query('stock_basic', exchange='', list_status='L',
                     fields='ts_code,symbol,name,area,industry,market,list_date')
    return data

def nameConvert(ts_name):
    '''

    :param ts_name: 000001.SZ
    :return:0000001.sz
    '''
    code,market = ts_name.split('.')
    market = str.lower(market)
    return market+'.'+code