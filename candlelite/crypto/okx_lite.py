import os
from candlelite.settings import read_settings
from candlelite.crypto._base import IO

settings = read_settings()
CANDLE_BASE_DIR = settings['CANDLE_BASE_DIR'][0]  # 根目录
__OKX_DATE_DIRNAME = settings['OKX_DATE_DIRNAME'][0]
__OKX_FILE_DIRNAME = settings['OKX_FILE_DIRNAME'][0]
# 以日期为单位的存储目录
OKX_CANDLE_DATE_BASE_DIR = os.path.join(CANDLE_BASE_DIR, __OKX_DATE_DIRNAME)
# 以文件为单位的存储目录
OKX_CANDLE_FILE_BASE_DIR = os.path.join(CANDLE_BASE_DIR, __OKX_FILE_DIRNAME)
# 时区
OKX_TIMEZONE = settings['OKX_TIMEZONE'][0]
# 默认时间粒度
OKX_DEFAULT_BAR = settings['OKX_DEFAULT_BAR'][0]


class OkxLite(IO):
    CANDLE_DATE_BASE_DIR = OKX_CANDLE_DATE_BASE_DIR
    CANDLE_FILE_BASE_DIR = OKX_CANDLE_FILE_BASE_DIR
    TIMEZONE = OKX_TIMEZONE
    BAR = OKX_DEFAULT_BAR
