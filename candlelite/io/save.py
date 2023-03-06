import os
import numpy as np
import pandas as pd
import datetime
from typing import Union, Literal
from candlelite.calculate import transform as _transform
from candlelite.calculate import valid as _valid
from candlelite.calculate import interval as _interval
from paux import date as _date
from candlelite import exception
from candlelite.io import path as _path

__all__ = ['save_candle_map_by_date', 'save_candle_map_by_file', 'save_candle_by_file', 'save_candle_by_date']


# 按照日期保存Candle
def save_candle_by_date(
        candle: np.array,
        instType: str,
        symbol: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        replace: bool = True,
        drop_duplicate: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
):
    '''
    边按照日期写入，边进行valid，如果valid报告错误，之前的数据可以成功写入，后面的数据则不会继续写入
    '''

    # 去重排序
    if drop_duplicate or sort:
        candle = _transform.to_candle(candle, drop_duplicate=True, sort=True)
    # 验证数据
    date_range = _date.get_range_dates(start=start, end=end, timezone=timezone)
    for date in date_range:
        # 路径
        path = _path.get_candle_date_path(
            instType=instType,
            symbol=symbol,
            date=date,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir
        )
        # 不覆盖并且有文件，跳过
        if not replace and os.path.isfile(path):
            continue
        start_ts = _date.to_ts(date=date, timezone=timezone)
        end_ts = _date.tomorrow(date=date, timezone=timezone).timestamp() * 1000 - _interval.get_interval(bar)
        # end_ts = start_ts + 1000 * 60 * 60 * 24 - _interval.get_interval(bar=bar)

        candle_date = candle[
            (candle[:, 0] >= start_ts) & (candle[:, 0] <= end_ts)
            ]

        # 验证interval
        if valid_interval:
            valid_interval_result = _valid.valid_interval(candle=candle_date, bar=bar)
            if not valid_interval_result['code']:
                raise exception.CandleIntervalError(
                    symbol=symbol,
                    msg=valid_interval_result['msg']
                )
        # 验证start
        if valid_start:
            start_ts = _date.to_ts(date=date, timezone=timezone)
            valid_start_result = _valid.valid_start(candle=candle_date, start=start_ts, timezone=timezone)
            if not valid_start_result['code']:
                raise exception.CandleStartError(
                    symbol=symbol,
                    msg=valid_start_result['msg'],
                )
        # 验证end
        if valid_end:
            # end_ts = _date.to_ts(date=date, timezone=timezone) + 1000 * 60 * 60 * 24 - _interval.get_interval( bar)
            end_ts = _date.tomorrow(date=date, timezone=timezone).timestamp() * 1000 - _interval.get_interval(bar)
            valid_end_result = _valid.valid_end(candle=candle_date, end=end_ts, timezone=timezone)
            if not valid_end_result['code']:
                raise exception.CandleEndError(
                    symbol=symbol,
                    msg=valid_end_result['msg'],
                )

        dirpath = os.path.dirname(path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        df_date = pd.DataFrame(candle_date)
        df_date.to_csv(path, index=False)


# 按照日期保存candle_map
def save_candle_map_by_date(
        candle_map: dict,
        instType: str,
        symbols: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        drop_duplicate: bool = True,
        replace: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
):
    '''
    如果写入的时候出现了错误，报错之前写入成功，报错后面的则不能正常写入
    '''
    if not symbols:
        symbols = [symbol for symbol in candle_map.keys()]
    for symbol in symbols:
        candle = candle_map[symbol]
        save_candle_by_date(
            instType=instType,
            symbol=symbol,
            candle=candle,
            start=start,
            end=end,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
            replace=replace,
            drop_duplicate=drop_duplicate,
            sort=sort,
            valid_interval=valid_interval,
            valid_start=valid_start,
            valid_end=valid_end,
        )


# 按照文件地址保存Candle
def save_candle_by_file(
        candle: np.array,
        instType: str,
        symbol: str,
        path: str = None,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        replace: bool = True,
        sort=True,
        drop_duplicate=True,
        valid_interval=True,
):
    # 得到路径
    if path == None:
        path = _path.get_candle_file_path(
            instType=instType,
            symbol=symbol,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    # 不覆盖并且有文件，跳过
    if not replace and os.path.isfile(path):
        return None

    # 验证interval
    if valid_interval:
        valid_interval_result = _valid.valid_interval(candle=candle, bar=bar)
        if not valid_interval_result['code']:
            raise exception.CandleIntervalError(
                symbol=symbol,
                msg=valid_interval_result['msg']
            )

    # 排序去重
    if sort or valid_interval:
        candle = _transform.to_candle(
            candle=candle,
            drop_duplicate=drop_duplicate,
            sort=sort
        )
    # 文件夹与路径
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    df = pd.DataFrame(candle)
    # 写入文件
    df.to_csv(path, index=False)


# 按照文件地址保存Candle_map
def save_candle_map_by_file(
        candle_map: dict,
        instType: str,
        symbols: list,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        replace: bool = True,
        sort: bool = True,
        drop_duplicate: bool = True,
        valid_interval: bool = True,
):
    # symbols
    if not symbols:
        symbols = [symbol for symbol in candle_map.keys()]

    for symbol in symbols:
        candle = candle_map[symbol]
        save_candle_by_file(
            candle=candle,
            instType=instType,
            symbol=symbol,
            path=None,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            replace=replace,
            sort=sort,
            drop_duplicate=drop_duplicate,
            valid_interval=valid_interval,
        )
