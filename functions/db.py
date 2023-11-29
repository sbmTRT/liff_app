import logging
# import cx_Oracle
import inspect
import time
from datetime import datetime
from logging import FileHandler

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

from configs import log_config
from utils.log_utils import *

env = Env()
env.read_env()

YMD = '{:%Y-%m-%d}'.format(datetime.now())

LOG_BACKUP_COUNT = int(env('LOG_BACKUP_COUNT'))

DATABASE_URL = env('DATABASE_URL')

# DBログ出力設定
logger = logging.getLogger('sqlalchemy.engine')
format = '%(asctime)s [%(levelname)s] %(message)s'
handler = FileHandler(log_config.SQL_LOG_PATH)
logger.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)

# DB接続処理
engine = create_engine(DATABASE_URL, echo=False, max_identifier_length=128)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()
