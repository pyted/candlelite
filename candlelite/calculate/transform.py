'''
compress_candle             压缩历史K线
extract_candle              根据时间跨度截取K线
concat_candle               合并数据
to_candle                   转换为ndarray类型的K数据
get_candle_index_by_date    根据日期时间，得到K线中的行索引
'''

from typing import Union
import datetime
import numpy as np
import pandas as pd
from paux import date as _date
from candlelite import exception
from candlelite.calculate import bar as _bar
from candlelite.calculate import interval as _interval

__all__ = ['compress_candle', 'extract_candle', 'to_candle', 'concat_candle', 'get_candle_index_by_date']


# 压缩历史K线
def compress_candle(
        candle: np.array,
        target_bar: str,
        org_bar: str = 'auto'
) -> np.ndarray:
    '''
    :param candle: 历史K线数据
    :param target_bar: 目标K线的bar
    :param org_bar: 原始K线的bar
       auto: 自动识别原始K线的bar
    :return:压缩后的历史K线数据
        array([
            [ts,open,high,low,close,volume...],
            [ts,open,high,low,close,volume...],
            [ts,open,high,low,close,volume...],
        ])
    example：
        将1Minute的K线数据压缩成5Minute的K线数据
        compress_candle(candle,target_bar='5m',org_bar='1m')

        将1Hour的K线数据压缩成1Day的K线数据
        compress_candle(candle,target_bar='1d',org_bar='1h'
    '''
    if org_bar == 'auto':
        org_bar = _bar.predict_bar(candle)
    # 目标K线ts间隔
    target_bar_interval = _interval.get_interval(target_bar)
    # 原始K线ts间隔
    org_tar_interval = _interval.get_interval(org_bar)
    # 压缩的数量
    compress_quantity = target_bar_interval / org_tar_interval
    if compress_quantity != int(compress_quantity):
        raise exception.ExecuteException(
            func='compress_candle',
            msg="Can't transform candle from org_bar=({org_bar}) to target_bar={target_bar}".format(
                org_bar=org_bar,
                target_bar=target_bar,
            )
        )
    compress_quantity = int(compress_quantity)
    # 目标K线数据
    target_datas = []
    candle_shape = candle.shape
    for i in range(0, candle.shape[0], compress_quantity):
        if i + compress_quantity <= candle_shape[0]:
            this_data = [
                candle[i, 0],  # ts
                candle[i, 1],  # open
                candle[i:i + compress_quantity, 2].max(),  # high
                candle[i:i + compress_quantity, 3].min(),  # low
                candle[i + compress_quantity - 1, 4],  # close
                candle[i:i + compress_quantity, 5].sum()  # volume
            ]
            # 如果有其他数据
            for i in range(6, candle_shape[1]):
                this_data.append(
                    candle[i:i + compress_quantity, i].sum()
                )
            target_datas.append(this_data)
    # 目标K线Candle
    target_candle = np.array(target_datas)
    return target_candle


# 根据时间跨度截取candle
def extract_candle(
        candle: np.array,
        start: Union[int, float, str, datetime.date, None],
        end: Union[int, float, str, datetime.date, None],
        timezone: Union[str, None] = None,
) -> np.ndarray:
    '''
    :param candle: 历史K线数据
    :param start: 数据起点 (包含起点）
    :param end: 数据终点 (包含终点）
    :param timezone: 时区
    '''
    start_ts = _date.to_ts(date=start, timezone=timezone, default=0)
    end_ts = _date.to_ts(date=end, timezone=timezone, default=candle[:, 0].max())
    return candle[(candle[:, 0] >= start_ts) & (candle[:, 0] <= end_ts)]


# 转换为candle数据
def to_candle(
        candle: Union[list, tuple, np.ndarray, pd.DataFrame],
        drop_duplicate: bool = True,
        sort: bool = True
) -> np.ndarray:
    '''
    :param candle: 历史K线数据，支持列表、元组、array、DataFrame
    :param drop_duplicate: 去重
    :param sort: 排序
    '''
    # list和tuple
    if isinstance(candle, list) or isinstance(candle, tuple):
        df = pd.DataFrame(candle)
    # DataFrame
    elif isinstance(candle, pd.DataFrame):
        df = candle
    # Array
    elif isinstance(candle, np.ndarray):
        df = pd.DataFrame(candle)
    # 未知类型
    else:
        raise exception.ParamException(
            func='to_candle',
            msg='input candle type is {candle_type}, candle type must in [list,tuple,pd.DataFrame,np.ndarray]'.format(
                candle_type=type(candle).__name__
            )
        )
    # 时间序列的名字
    ts_column_name = df.columns[0]
    # 时间戳转化为整数
    df[ts_column_name] = df[ts_column_name].astype(float)
    # 去重
    if drop_duplicate:
        df = df.drop_duplicates(subset=ts_column_name)
    # 排序
    if sort:
        df = df.sort_values(by=ts_column_name)
    # 转化为array对象
    candle = df.to_numpy()
    return candle


# 合并数据
def concat_candle(
        candles: list,
        drop_duplicate: bool = True,
        sort: bool = True
) -> np.ndarray:
    '''
    :param candles: 多个历史K线数据
    :param drop_duplicate: 去重
    :param sort: 排序
    '''
    for i in range(len(candles)):
        # list和tuple
        if isinstance(candles[i], list) or isinstance(candles[i], tuple):
            candles[i] = pd.DataFrame(candles[i])
        # DataFrame
        elif isinstance(candles[i], pd.DataFrame):
            pass
        # Array
        elif isinstance(candles[i], np.ndarray):
            candles[i] = pd.DataFrame(candles[i])
        # 未知类型
        else:
            raise exception.ParamException(
                func='concat_candle',
                msg='input candle type is {candle_type}, candle type must in [list,tuple,pd.DataFrame,np.ndarray]'.format(
                    candle_type=type(candles[i]).__name__
                ),
            )
    # 拼接数据
    df = pd.concat(candles)
    candle = to_candle(candle=df, drop_duplicate=drop_duplicate, sort=sort)
    return candle


# 根据日期时间，得到K线中的行索引
def get_candle_index_by_date(
        candle: np.array,
        date: Union[datetime.datetime, int, float, str,],
        timezone: str = None,
        default: int = 0
) -> int:
    '''
    :param candle: 历史K线数据
    :param date: 日期时间
    :param timezone: 时区
    :param default: 默认值
    :return: 航索引
    '''
    if not date:
        return default
    ts = _date.to_ts(date=date, timezone=timezone, default=default)
    index = np.where(
        candle[:, 0] == ts
    )[0][0]
    return index
