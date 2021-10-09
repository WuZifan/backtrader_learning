import datetime
import time

import akshare as ak
import pandas as pd
import sqlalchemy
from sqlalchemy import log
from tqdm import tqdm

from sqlalchemy import func
from dataUpdate import logger, engine
from dataUpdate.model.basicinfo import StockBasic, StockEarningReport
from dataUpdate.model.tradingInfo import TradingInfo
from dataUpdate.util import ts_util, jq_util, bs_util

date_formate = '%Y-%m-%d'
'''
    1、更新数据库中的stockbasic表，添加开始时间和结束时间
    2、利用代码来更新stockbasic表中的开始时间和结束时间
    3、更新交易信息时：
        3.1 从stockbasic中获取全量股票名称，开始时间和结束时间
        3.2 如果开始时间和结束时间不为None，那么添加结束时间+1天到今天的交易信息
        3.3 如果开始时间和结束时间为None，那么添加20050101 到今天的交易信息
'''


def update_single_stock_tradinginfo(sess,stock_code='sh.600000',start_date='2010-01-01',end_date='2020-12-31'):
    """更新单个股票的交易数据

    Args:
        sess ([type]): [description]
        stock_code (str, optional): [description]. Defaults to 'sh.600000'.
        start_date (str, optional): [description]. Defaults to '2010-01-01'.
        end_date (str, optional): [description]. Defaults to '2020-12-31'.
    """
    


    stock_trading_infos = sess.query(func.min(TradingInfo.time),func.max(TradingInfo.time)).filter(TradingInfo.code==stock_code).all()

    if len(stock_trading_infos)==0:
        start_date_str = start_date
        end_date_str = end_date
    else:
        input_start_date = datetime.datetime.strptime(start_date,date_formate)
        input_end_date = datetime.datetime.strptime(end_date,date_formate)

        db_start_date = stock_trading_infos[0][0]
        db_end_date = stock_trading_infos[0][1]

        if db_start_date<=input_start_date and input_end_date<=db_end_date:
            logger.info("Stock {stockname} trading data between {startdate} and {enddate} already exists"
            .format(stockname=stock_code,startdate=start_date,enddate=end_date))
        else:
            start_date = db_start_date if db_start_date<=input_start_date else input_start_date
            end_date = db_end_date if db_end_date>=input_end_date else input_end_date

            # 删除数据
            sess.query(TradingInfo).filter(TradingInfo.code==stock_code).delete()

            # 写入数据
            start_date_str = start_date.strftime(date_formate)
            end_date_str = end_date.strftime(date_formate)
            temp_df = bs_util.getStockHistoryInfo(stock_code, start_date_str, end_date_str)
            temp_df.to_sql(TradingInfo.__tablename__, con=engine, if_exists='append', index=False)
            sess.commit()
            logger.info("Stock {stockname} trading data updates! Now its between {startdate} and {enddate}"
            .format(stockname=stock_code,startdate=start_date,enddate=end_date))

def update_stock_tradinginfo(sess):
    '''
    更新全量股票数据
    :param sess:
    :return:
    '''

    bs_util.login_bs()

    # 1、获取全部股票代码
    # sql = sess.query(StockBasic.code,StockBasic.start_time,StockBasic.end_time)
    stock_codes = sess.query(StockBasic).all()
    # stock_codes = pd.read_sql(sql.statement, sql.session.bind)

    # logger.debug(stock_codes.head())
    t1 = time.time()
    # 3、根据已有股票的最新日期，来更新他们的数据
    for stk in tqdm(stock_codes):
        # 3.1 计算需要获取的股票起始和结束时间
        stock_code, start_date, end_date = stk.code, stk.start_time, stk.end_time
        if isinstance(end_date, datetime.datetime):
            start_date = end_date + datetime.timedelta(days=1)
            end_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime(2005, 1, 1)
            end_date = datetime.datetime.now()

        if start_date >= end_date:
            continue
        start_date_str = start_date.strftime(date_formate)
        end_date_str = end_date.strftime(date_formate)

        # 3.2 查询数据
        temp_df = bs_util.getStockHistoryInfo(stock_code, start_date_str, end_date_str)
        if len(temp_df) == 0:
            logger.info('Nothing to update for {} between {} and {}'.format(stock_code, start_date_str, end_date_str))
        # 3.3 插入数据库 600905
        temp_df.to_sql(TradingInfo.__tablename__, con=engine, if_exists='append', index=False)

        # 3.4 更新股票的开始结束时间
        stk.end_time = end_date
        # stk.start_time = start_date

    t2 = time.time()
    logger.info("Update existing stock cost {}".format(t2 - t1))
    sess.commit()


def update_stock_basic(sess):
    '''
    将新的股票信息加入，主要步骤如下：
        1、表结构见 StockBasic类
        2、通过tushare查询获得所有最新的股票数据
        3、查数据库获取已有股票信息
        3、找到新增的股票数据
        4、获取股票的基础信息，并通过聚宽的API来查询该股票的3级行业分类和流通市值以及股本
    :param sess:
    :return:
    '''

    # 1、通过tushare获得最新的股票数据
    latest_stock = ts_util.getStockBasicInfo()
    latest_stock['ts_code'] = latest_stock['ts_code'].apply(ts_util.nameConvert)
    logger.info('latest stock number {}'.format(len(latest_stock)))
    logger.debug(latest_stock.head())

    # 2、通过数据库连接获得已有的股票信息
    sql = sess.query(StockBasic.code)
    res_df = pd.read_sql(sql.statement, sql.session.bind)
    logger.info('stored stock number {}'.format(len(res_df)))

    # 3、求差集，获取新增的股票
    new_stock = list(set(list(latest_stock['ts_code'])) - set(list(res_df['code'])))
    logger.info('new stock number {}'.format(len(new_stock)))
    logger.debug(new_stock)

    # 4、将新股票的信息写入数据库
    ns_list = []
    for ts_code in tqdm(new_stock):

        # 4.1 获取基础信息
        temp_ins = latest_stock[latest_stock['ts_code'] == ts_code]
        # print(temp_ins)
        temp_symbol = temp_ins['symbol'].item()
        temp_name = temp_ins['name'].item()
        temp_area = temp_ins['area'].item()
        temp_ind = temp_ins['industry'].item()
        temp_market = temp_ins['market'].item()
        temp_ld = temp_ins['list_date'].item()

        # 4.2 获取jq_code
        jq_code = jq_util.getJQCode(ts_code)

        # 4.3 获取申万3级分类
        try:
            d = jq_util.get_industry(jq_code)
            sw_l3 = d[jq_code]['sw_l3']['industry_name']
            sw_l1 = d[jq_code]['sw_l1']['industry_name']
        except Exception as e:
            sw_l1 = None
            sw_l3 = None
            logger.error(ts_code, ' no sw_l1 or sw_l3')

        # 4.4 获取流通市值和股本
        q = jq_util.query(
            jq_util.valuation.code,
            # valuation.day,
            # valuation.market_cap, # 总市值
            jq_util.valuation.circulating_market_cap,  # 流通市值
            # valuation.capitalization,# 总股本
            jq_util.valuation.circulating_cap  # 流通总股本
        ).filter(
            jq_util.valuation.code.in_([jq_code]),
        )
        # 不填日期，这里展示最新的数据
        ret = jq_util.get_fundamentals(q)
        try:
            circulating_cap = float(ret.iloc[0]['circulating_cap'])
            circulating_market_cap = float(ret.iloc[0]['circulating_market_cap'])
        except Exception as e:
            circulating_cap = None
            circulating_market_cap = None
            logger.error('stock {} does not have circulating cap info {}'.format(ts_code, ret))

        temp_stockbasic = StockBasic(ts_code, temp_symbol, temp_name,
                                     temp_area, temp_ind,
                                     temp_market, temp_ld, sw_l1,sw_l3,
                                     circulating_market_cap, circulating_cap)
        # print(temp_stockbasic)
        ns_list.append(temp_stockbasic)

    # 写入数据库
    sess.add_all(ns_list)
    sess.commit()

    # 查看更新后数量
    sql = sess.query(StockBasic.code)
    res_df = pd.read_sql(sql.statement, sql.session.bind)
    logger.info('after update stored stock number {}'.format(len(res_df)))
    return res_df


def update_stock_earning_report(sess):
    '''
    用一个很蠢的办法，直接覆盖
        1、每次都获取起始日期到当前的苏搜you财报信息
        2、获取完成后就直接覆盖全表
    :param sess:
    :return:
    '''
    start_year = 2010
    end_year = datetime.datetime.now().year
    days = ['0331', '0630', '0930', '1231']
    final_df = pd.DataFrame()
    dateformat = '%Y%m%d'
    flag = False
    for year in range(start_year, end_year + 1):
        for day in days:
            temp_date = str(year) + day
            logger.info(temp_date)
            temp_compare_date = datetime.datetime.strptime(temp_date,dateformat)
            if temp_compare_date>=datetime.datetime.now():
                flag=True
                break
            temp_result = ak.stock_em_yjbb(date=temp_date)
            temp_result.rename(columns={
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
            },inplace=True)
            temp_result = temp_result[['id','code','earning_per_share',
                                       'revenue','revenue_yoy_rise','revenue_sos_rise',
                                       'net_profit','net_profit_yoy_rise','net_profit_sos_rise',
                                       'return_on_equity','operating_cash_flow_per_share',
                                       'gross_profit_ratio']]
            temp_result['year'] = year
            temp_result['date'] = day
            final_df = pd.concat([final_df,temp_result],ignore_index=True)

        if flag:
            break
    final_df['id'] = list(range(1,len(final_df)+1))
    final_df.to_sql(StockEarningReport.__tablename__, con=engine, if_exists='replace', index=False)
    sess.commit()