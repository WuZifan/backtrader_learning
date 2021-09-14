import datetime
import time

import akshare as ak
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from sqlalchemy import func
from dataUpdate import logger, engine
from dataUpdate.model.basicinfo import StockBasic, StockEarningReport
from dataUpdate.model.tradingInfo import TradingInfo
from dataUpdate.util import ts_util, jq_util, bs_util

'''
    仅用于临时使用，使用场景：
        1、数据表新增一列，不想全表覆盖，就在这里新写方法来拉数据填入
'''

def temp_update_stock_basic_with_swl1(sess):
    jq_util.login_jq()
    stocks = sess.query(StockBasic).all()
    for stk in tqdm(stocks):
        jq_code = jq_util.getJQCode(stk.code)

        d = jq_util.get_industry(jq_code)
        try:
            sw_l1 = d[jq_code]['sw_l1']['industry_name']
            stk.sw_l1 = sw_l1
        except Exception as e:
            logger.info("stock {} does not have sw_l1.".format(stk.code))

    sess.commit()




