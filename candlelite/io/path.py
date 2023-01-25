from typing import Literal, Union
import os
import re
import datetime
from paux import date as _date

__all__ = [
    'get_candle_date_path',  # 获取某一个天candle的路径
    'get_candle_file_path',  # 获取candle文件的地址（一般不以天切割，必须缓存数据与1d数据可以储存在一个文件中）
    'check_candle_date_path',  # 检查candle文件是否存在（不验证数据的准确性）
    'check_candle_file_path',  # 检查candle从start到end日期数据文件是否齐全（仅检查文件是否存在，并不验证文件的准确性）
]


# 将instType、timezone与bar转换成文件夹的名字
def _get_date_dirname(
        instType: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m'
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param bar: 时间粒度
    :return: 文件夹的名字（并不是文件夹的路径）
    '''
    if timezone == None:
        timezone = ''
    timezone = re.sub('/', '', timezone)
    return '-'.join([instType, timezone, bar])


# 将instType、timezone与bar转换成文件夹的名字
def _get_file_dirname(
        instType: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m'
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param bar: 时间粒度
    :return: 文件夹的名字（并不是文件夹的路径）
    '''
    if timezone == None:
        timezone = ''
    timezone = re.sub('/', '', timezone)
    return '-'.join([instType, timezone, bar, 'FILE'])


# 获取某一个天candle的路径
def get_candle_date_path(
        instType: str,
        symbol: str,
        date: datetime.date,
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param date: 日期
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :return: 某产品在指定日期的candle数据路径
    '''
    FMT = '%Y-%m-%d'
    date_str = _date.to_fmt(date=date, timezone=timezone, fmt=FMT)
    filepath = os.path.join(
        base_dir,
        _get_date_dirname(instType=instType, timezone=timezone, bar=bar),
        date_str[0:7],
        date_str,
        '%s.csv' % symbol
    )
    return filepath


# 获取candle文件的地址（一般不以天切割，必须缓存数据与1d数据可以储存在一个文件中）
def get_candle_file_path(
        instType: str,
        symbol: str,
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :return: candle文件的路径
    '''
    FMT = '{symbol}.csv'
    filepath = os.path.join(
        base_dir,
        _get_file_dirname(instType=instType, timezone=timezone, bar=bar),
        FMT.format(symbol=symbol)
    )
    return filepath


# 检查candle文件是否存在（不验证数据的准确性）
def check_candle_file_path(
        instType: str,
        symbol: str,
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :return:
        True    有文件
        False   无文件
    '''
    path = get_candle_file_path(
        instType=instType,
        symbol=symbol,
        base_dir=base_dir,
        timezone=timezone,
        bar=bar
    )
    result = {
        'code': os.path.isfile(path),
        'data': path,
        'msg': path,
    }
    return result


# 检查candle从start到end日期数据文件是否齐全（仅检查文件是否存在，并不验证文件的准确性）
def check_candle_date_path(
        instType: str,
        symbol: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir:str ='',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    '''
    :param instType: 产品类别
    :param symbol: 产品名称
    :param start: 起始日期
    :param end: 终止日期（包含）
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :return:
        code:
            True    数据齐全
            False   数据不全
    '''
    dates = _date.get_range_dates(start=start, end=end, timezone=timezone)
    result = {'code': True, 'data': [], 'msg': ''}  # data保存不存在数据的日期与路径

    for date in sorted(dates, reverse=True):
        path = get_candle_date_path(
            instType=instType, symbol=symbol, date=date,
            timezone=timezone, base_dir=base_dir, bar=bar
        )
        if not os.path.isfile(path):
            result['code'] = False
            result['data'].append(
                {
                    'date': date,
                    'path': path,
                }
            )
    return result


