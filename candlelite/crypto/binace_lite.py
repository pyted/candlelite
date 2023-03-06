import os
from candlelite.settings import read_settings
from candlelite.crypto._base import IO

settings = read_settings()
CANDLE_BASE_DIR = settings['CANDLE_BASE_DIR'][0]  # 根目录
__BINANCE_DATE_DIRNAME = settings['BINANCE_DATE_DIRNAME'][0]
__BINANCE_FILE_DIRNAME = settings['BINANCE_FILE_DIRNAME'][0]
# 以日期为单位的存储目录
BINANCE_CANDLE_DATE_BASE_DIR = os.path.join(CANDLE_BASE_DIR, __BINANCE_DATE_DIRNAME)
# 以文件为单位的存储目录
BINANCE_CANDLE_FILE_BASE_DIR = os.path.join(CANDLE_BASE_DIR, __BINANCE_FILE_DIRNAME)
# 时区
BINANCE_TIMEZONE = settings['BINANCE_TIMEZONE'][0]
# 默认时间粒度
BINANCE_DEFAULT_BAR = settings['BINANCE_DEFAULT_BAR'][0]

class BinanceLite(IO):
    CANDLE_DATE_BASE_DIR = BINANCE_CANDLE_DATE_BASE_DIR
    CANDLE_FILE_BASE_DIR = BINANCE_CANDLE_FILE_BASE_DIR
    TIMEZONE = BINANCE_TIMEZONE
    BAR = BINANCE_DEFAULT_BAR
