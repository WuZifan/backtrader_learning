from sqlalchemy.ext.declarative import declarative_base  # db 基类
from sqlalchemy import create_engine
import json
import logging
import sys
import os


# 数据库相关
with open('./config.json','r') as f:
    mysqlConfig = json.load(f)

SQLALCHEMY_DATABASE_URI ="mysql+pymysql://{username}:{passsword}@{host}:{port}/{database}?charset=utf8&use_unicode=1".format(
                username = mysqlConfig['username'],
                passsword = mysqlConfig['password'],
                host = mysqlConfig['host'],
                port = mysqlConfig['port'],
                database = mysqlConfig['database']
            )

engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=5,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）,
                       echo=False)

Base = declarative_base(bind=engine)

# 日志相关

BASIC_FORMAT = "%(asctime)s:\t%(levelname)s:\t%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler() # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('DEBUG')

logger = logging.getLogger(name='dataUpdate')
logger.setLevel(logging.DEBUG)
logger.addHandler(chlr)