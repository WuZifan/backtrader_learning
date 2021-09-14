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

    tempUpdateService.temp_update_stock_basic_with_swl1(sess)
