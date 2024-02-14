from typing import Union, Literal
import os
import numpy as np
import pandas as pd
import datetime
from paux import param as _param
from paux import process as _process
from paux import date as _date
from candlelite.calculate import transform as _transform
from candlelite.calculate import valid as _valid
from candlelite.calculate import interval as _interval
from candlelite.io import path as _path
from candlelite import exception

__all__ = [
    'load_candle_by_date',
    'load_candle_by_file',
    'load_candle_map_by_date',
    'load_candle_map_by_file',
]


# 读取从start~end日期的历史K线数据
def load_candle_by_date(
        instType: str,
        symbol: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        columns: list = [],
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
) -> np.ndarray:
    '''
    :param instType: 产品类型
    :param symbol: 产品名称
    :param start: 起始时间
    :param end: 终止时间
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :parma columns: 保留字段，保留candle中的哪些列，空列表表示全部
    :param valid_interval: 是否验证数据时间间隔
    :param valid_start: 是否验证数据起始时间
    :param valid_end: 是否验证数据终止时间
    '''
    # 文件是否存在
    check_result = _path.check_candle_date_path(
        instType=instType,
        symbol=symbol,
        start=start,
        end=end,
        timezone=timezone,
        bar=bar,
        base_dir=base_dir,
    )
    if not check_result['code']:
        raise exception.CandleFileNotExist(
            symbol=symbol,
            date=str([data['date'] for data in check_result['data']]),
            path=None,

        )
    # 日期序列
    date_range = _date.get_range_dates(
        start=start,
        end=end,
        timezone=timezone,
    )
    # 文件路径
    paths = [
        _path.get_candle_date_path(
            instType=instType,
            symbol=symbol,
            date=date,
            timezone=timezone,
            bar=bar,
            base_dir=base_dir,
        )
        for date in date_range
    ]
    # 读取->DataFrame
    dfs = [pd.read_csv(path) for path in paths]
    # 合并数据->Candle
    candle = _transform.concat_candle(candles=dfs, drop_duplicate=True, sort=True)
    # 验证interval
    if valid_interval:
        valid_interval_result = _valid.valid_interval(candle=candle, bar=bar)
        if not valid_interval_result['code']:
            raise exception.CandleIntervalError(
                symbol=symbol,
                msg=valid_interval_result['msg']
            )
    # 验证start
    if valid_start:
        start_ts = _date.to_ts(date=date_range[0], timezone=timezone)
        valid_start_result = _valid.valid_start(candle=candle, start=start_ts, timezone=timezone)
        if not valid_start_result['code']:
            raise exception.CandleStartError(
                symbol=symbol,
                msg=valid_start_result['msg'],
            )
    # 验证end
    if valid_end:
        end_ts = _date.tomorrow(date=date_range[-1], timezone=timezone).timestamp() * 1000 - _interval.get_interval(bar)
        # end_ts = _date.to_ts(date=date_range[-1], timezone=timezone) + 1000 * 60 * 60 * 24 - _interval.get_interval(bar)
        valid_end_result = _valid.valid_end(candle=candle, end=end_ts, timezone=timezone)
        if not valid_end_result['code']:
            raise exception.CandleEndError(
                symbol=symbol,
                msg=valid_end_result['msg'],
            )
    if columns:
        candle = candle[:, columns]

    return candle


# 按照日期读取candle_map
def load_candle_map_by_date(
        instType: str,
        symbols: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        columns: list = [],
        endswith: str = '',
        contains: str = '',
        p_num: int = 1,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
) -> dict:
    '''
    :param instType: 产品类型
    :param symbols: 产品名称列表
    :param start: 起始时间
    :param end: 终止时间
    :param base_dir: 数据文件夹
    :param timezone: 时区
    :param bar: 时间粒度
    :parma columns: 保留字段，保留candle中的哪些列，空列表表示全部
    :param endswith: 产品名称需以此结尾
    :param contains: 产品名称需包含此内容
    :param valid_interval: 是否验证数据时间间隔
    :param valid_start: 是否验证数据起始时间
    :param valid_end: 是否验证数据终止时间
    '''
    # 如果没有产品的名字，获取产品类型数据中，有start_date到end_date中有完整数据的symbol
    if not symbols:
        dates = _date.get_range_dates(start=start, end=end, timezone=timezone)
        symbols = set()
        for date in dates:
            date_dirpath = os.path.dirname(
                _path.get_candle_date_path(
                    base_dir=base_dir,
                    instType=instType,
                    timezone=timezone,
                    date=date,
                    bar=bar,
                    symbol=''
                )
            )
            this_symbols = []
            for filename in os.listdir(date_dirpath):
                symbol = filename.rsplit('.', maxsplit=1)[0]
                if endswith and not symbol.endswith(endswith):
                    continue
                if contains and not contains in symbol:
                    continue
                else:
                    this_symbols.append(symbol)
            if not symbols:
                symbols = set(this_symbols)
            else:
                symbols = symbols & set(this_symbols)
    symbols = list(symbols)

    candle_map = {}
    if p_num > 1:
        params = []
        for symbol in symbols:
            params.append(
                dict(
                    instType=instType,
                    symbol=symbol,
                    start=start,
                    end=end,
                    timezone=timezone,
                    bar=bar,
                    columns=columns,
                    base_dir=base_dir,
                    valid_interval=valid_interval,
                    valid_start=valid_start,
                    valid_end=valid_end,
                )
            )
        results = _process.pool_worker(
            params=params,
            p_num=p_num,
            func=load_candle_by_date,
            skip_exception=False,
        )
        for i, candle in enumerate(results):
            if _param.isnull(candle):
                continue
            symbol = symbols[i]
            candle_map[symbol] = candle

    else:
        for symbol in symbols:
            candle_map[symbol] = load_candle_by_date(
                instType=instType,
                symbol=symbol,
                start=start,
                end=end,
                timezone=timezone,
                bar=bar,
                columns=columns,
                base_dir=base_dir,
                valid_interval=valid_interval,
                valid_start=valid_start,
                valid_end=valid_end,
            )
    # candle_map排序
    candle_map_sorted = {}
    symbols = sorted([symbol for symbol in candle_map.keys()])
    for symbol in symbols:
        candle_map_sorted[symbol] = candle_map[symbol]
    return candle_map_sorted


# 加载一个产品已有的全部K线
def load_candle_all(
        instType: str,
        symbol: str,
        base_dir: str,
        columns: list = [],
        start: Union[int, float, str, datetime.date] = None,
        end: Union[int, float, str, datetime.date] = None,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    candle_dates_result = _path.get_candle_dates(
        instType=instType,
        symbol=symbol,
        start=start,
        end=end,
        base_dir=base_dir,
        timezone=timezone,
        bar=bar,
    )

    if candle_dates_result['code'] != True:
        raise exception.CandleDatesNonError(str(candle_dates_result))
    # 空数据
    if not candle_dates_result['data']['start'] or not candle_dates_result['data']['end']:
        return np.array([])
    candle = load_candle_by_date(
        instType=instType,
        start=candle_dates_result['data']['start'],
        end=candle_dates_result['data']['end'],
        symbol=symbol,
        base_dir=base_dir,
        timezone=timezone,
        bar=bar,
        columns=columns,
    )
    return candle


# 加载全部产品已有的K线
def load_candle_map_all(
        instType: str,
        base_dir: str,
        symbols: list = [],
        endswith: str = '',
        contains: str = '',
        start: Union[int, float, str, datetime.date] = None,
        end: Union[int, float, str, datetime.date] = None,
        timezone: str = None,
        p_num: int = 1,
        columns: list = [],
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    if not symbols:
        symbols = _path.get_symbols_all(
            instType=instType,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
        )
        # 过滤endswith与contains
        symbols = [symbol for symbol in symbols if symbol.endswith(endswith) and contains in symbol]

    candle_map = {}
    if p_num > 1:
        params = []
        for symbol in symbols:
            params.append(
                dict(
                    instType=instType,
                    symbol=symbol,
                    base_dir=base_dir,
                    timezone=timezone,
                    bar=bar,
                    columns=columns,
                    start=start,
                    end=end,
                )
            )
        results = _process.pool_worker(
            params=params,
            p_num=p_num,
            func=load_candle_all,
            skip_exception=False,
        )
        for i, candle in enumerate(results):
            if _param.isnull(candle):
                continue
            if not candle.shape[0]:
                continue
            symbol = symbols[i]
            candle_map[symbol] = candle
    else:
        for symbol in symbols:
            candle = load_candle_all(
                instType=instType,
                symbol=symbol,
                base_dir=base_dir,
                start=start,
                end=end,
                timezone=timezone,
                bar=bar,
                columns=columns,
            )
            if not candle.shape[0]:
                continue
            candle_map[symbol] = candle
    return candle_map


# 通过文件地址读取Candle
def load_candle_by_file(
        instType: str,
        symbol: str,
        columns: list = [],
        path: str = None,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,
):
    '''
    如果有path路径，按照path路径读取文件
    如果没有path路径，按照base_dir、symbol、instType、bar和timezone计算产品路径
    '''
    # 路径
    if path == None:
        path = _path.get_candle_file_path(
            instType=instType,
            symbol=symbol,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    # 读取
    df = pd.read_csv(path)
    candle = _transform.to_candle(candle=df, drop_duplicate=True, sort=True)
    # 验证interval
    if valid_interval:
        valid_interval_result = _valid.valid_interval(candle=candle, bar=bar)
        if not valid_interval_result['code']:
            raise exception.CandleIntervalError(
                symbol=symbol,
                msg=valid_interval_result['msg']
            )
    if columns:
        candle = candle[:, columns]
    return candle


# 通过文件夹地址读取Candle_map
def load_candle_map_by_file(
        instType: str,
        symbols: list = [],
        columns=[],
        path: str = None,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,
):
    # 路径
    if path == None:
        path = os.path.dirname(
            _path.get_candle_file_path(
                instType=instType,
                base_dir=base_dir,
                timezone=timezone,
                bar=bar,
                symbol='xx',
            )
        )
    # symbols
    if not symbols:
        filenames = os.listdir(path)
        symbols = []
        for filename in filenames:
            symbol = filename.rsplit('.', maxsplit=1)[0]
            symbols.append(symbol)
    # 读取数据
    candle_map = {}
    for symbol in symbols:
        candle = load_candle_by_file(
            symbol=symbol,
            instType=instType,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            columns=columns,
            valid_interval=valid_interval
        )
        candle_map[symbol] = candle
    # candle_map排序
    candle_map_sorted = {}
    symbols = sorted([symbol for symbol in candle_map.keys()])
    for symbol in symbols:
        candle_map_sorted[symbol] = candle_map[symbol]
    return candle_map_sorted
