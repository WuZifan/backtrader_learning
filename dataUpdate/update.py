import sys
import os

sys.path.append('/Users/roland/vscode_program/backtrader_learning')
sys.path.insert(0,'/Users/roland/vscode_program/backtrader_learning/dataUpdate')

from sqlalchemy.orm import Session
from dataUpdate import engine
from dataUpdate.model.basicinfo import StockBasic
from dataUpdate.service import updateService
from dataUpdate.service import tempUpdateService
import sqlalchemy
from sqlalchemy import func
import time


def updatingStockBasicAndTradingInfo(sess):
    # 1、更新股票基本信息
    updateService.update_stock_basic(sess)

    # 2、更新股票交易信息
    updateService.update_stock_tradinginfo(sess)


def update_stock_earing_report(sess):
    # 3、更新股票报表数据
    updateService.update_stock_earning_report(sess)


if __name__ == '__main__':


    sess = Session(engine)

    all = sess.query(StockBasic).all()
    for stk in all:
        print(stk.code)
        break

    sess.close()
    # tempUpdateService.temp_update_stock_basic_with_swl1(sess)