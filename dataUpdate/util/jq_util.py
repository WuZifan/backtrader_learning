from jqdatasdk import *
from jqdatasdk import valuation


def market_map(market):
    '''
    上海证券交易所	.XSHG	'600519.XSHG'	贵州茅台
    深圳证券交易所	.XSHE	'000001.XSHE'	平安银行
    中金所	.CCFX	'IC9999.CCFX'	中证500主力合约
    大商所	.XDCE	'A9999.XDCE'	豆一主力合约
    上期所	.XSGE	'AU9999.XSGE'	黄金主力合约
    郑商所	.XZCE	'CY8888.XZCE'	棉纱期货指数
    上海国际能源期货交易所	.XINE	'SC9999.XINE'	原油主力合约
    :param market:
    :return:
    '''

    if market=='sh':
        return 'XSHG'
    elif market == 'sz':
        return 'XSHE'
    return None

def getJQCode(code):
    return normalize_code(code)


def getStockCirculating(stock_list = ['600519.XSHG']):
    if type(stock_list)!=list:
        stock_list = [stock_list]

    q = query(
        valuation.code,
        # valuation.day,
        # valuation.market_cap, # 总市值
        valuation.circulating_market_cap,  # 流通市值
        # valuation.capitalization,# 总股本
        # valuation.circulating_cap # 流通总股本
    ).filter(
        valuation.code.in_(stock_list),
    )
    ret = get_fundamentals(q)
    try:
        ret_val = list(ret['circulating_market_cap'])[0]
    except Exception as e:
        print(e)
        ret_val = 0
    return ret_val


def getTradingInfo(code,start_date,end_date):
    res = get_price(security=code, start_date=start_date, end_date=end_date, frequency='30m')
    return res

def login_jq():
    if not is_auth():
        auth('16675189576','wuzifan948173')
    else:
        print('Already login to JoinQuant')

# login_jq()

# if __name__ == '__main__':
#     login_jq()
#     # print(getStockCirculating())
#     jq_code= getJQCode('sh.605339')
#     print(jq_code)
#     q = query(
#         valuation.code,
#         # valuation.day,
#         # valuation.market_cap, # 总市值
#         valuation.circulating_market_cap,  # 流通市值
#         # valuation.capitalization,# 总股本
#         valuation.circulating_cap  # 流通总股本
#     ).filter(
#         valuation.code.in_([jq_code]),
#     )
#
#     ret = get_fundamentals(q)
#     print(ret)
