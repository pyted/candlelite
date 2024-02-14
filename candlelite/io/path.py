from typing import Literal, Union
import os
import re
import datetime
from paux import date as _date
from paux import file as _file

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
        base_dir: str = '',
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


# 获取candle具备数据的日期序列
def get_candle_dates(
        instType: str,
        symbol: str,
        start=None,
        end=None,
        base_dir: str = '',
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
        code:
            True    数据齐全
            False   数据不全
    '''
    result = {
        'code': True,
        'data': {
            'start': None,  # 数据起始
            'end': None,  # 数据终止
            'non': [],  # 缺失数据
        },
        'msg': ''
    }
    # 月份的文件夹地址
    month_dirpath = os.path.join(
        base_dir,
        _get_date_dirname(instType=instType, timezone=timezone, bar=bar),
    )
    # 年-月 序列
    year_months = [
        fn for fn in os.listdir(month_dirpath)
        if (os.path.isdir(os.path.join(month_dirpath, fn)))
           and (re.match('\d{4}-\d{2}', fn))
    ]
    year_months = sorted(year_months)
    if not year_months:
        result['code'] = False
        result['msg'] = '无数据'
        return result
    if not start:
        # 起始日期
        start = year_months[0] + '-01'
    if not end:
        days = _date.get_month_days(
            year=year_months[-1].split('-')[0],
            month=year_months[-1].split('-')[-1],
            timezone=timezone,
        )

        # 终止日期
        end = year_months[-1] + '-' + str(days)
    dates = _date.get_range_dates(start=start, end=end, timezone=timezone)
    candle_dates = []  # 有数据的日期
    for date in dates:
        path = get_candle_date_path(
            instType=instType, symbol=symbol, date=date,
            timezone=timezone, base_dir=base_dir, bar=bar
        )

        if os.path.isfile(path):
            candle_dates.append(date)
    if candle_dates:
        result['data']['start'] = candle_dates[0]
        result['data']['end'] = candle_dates[-1]
        range_dates = _date.get_range_dates(start=candle_dates[0], end=candle_dates[-1], timezone=timezone)
        for range_date in range_dates:
            if range_date not in candle_dates:
                result['data']['non'].append(range_date)
                result['code'] = False
        return result
    else:
        return result  # 没有数据，但是code=True start=None，end=None


# 获取全部的产品名称
def get_symbols_all(
        instType: str,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    filenames = _file.get_deep_filenames(
        dirpath=os.path.join(
            base_dir,
            _get_date_dirname(instType=instType, timezone=timezone, bar=bar),
        )
    )
    filenames = [fn.rsplit('.', maxsplit=1)[0] for fn in list(set(filenames)) if fn.endswith('.csv')]
    return filenames


if __name__ == '__main__':
    base_dir = '/Users/kzlknight/Documents/FINANCE_DATA/CANDLELITE_DATA/BINANCE'
    symbols = get_symbols_all(
        instType='UM',
        base_dir=base_dir,
        timezone='America/New_York'
    )
    print(symbols)
    for symbol in symbols:
        result_dates = get_candle_dates(
            instType='UM',
            symbol=symbol,
            base_dir=base_dir,
            timezone='America/New_York'
        )
        print(symbol, result_dates)
