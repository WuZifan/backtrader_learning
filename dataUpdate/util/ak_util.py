

# 0、添加股票市场名称
def convertAkCode2BSCode(stock):
    '''

        1、上交所：
            6开头 上交所;
            688开头，科创板，上交所
        2、深交所
            0开头，深交所
            002开头，中小板，也是深交所
            3开头 创业板，也是深交所
    :param stock:
    :return:
    '''
    stock = str(stock)
    assert len(stock)==6

    if stock.startswith('6'):
        return 'sh.'+stock
    elif stock.startswith('0') or stock.startswith('3'):
        return 'sz.'+stock