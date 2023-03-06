from typing import Union
import datetime
import numpy as np
import pandas as pd
from paux import date as _date
from paux.param import isnull
from candlelite import exception
from candlelite.calculate import interval as _interval

__all__ = ['valid_interval', 'valid_start', 'valid_end', 'valid_length']


# 验证数据间隔
def valid_interval(
        candle: np.array,
        interval: Union[int, float] = None,
        bar: str = None,
        MINUTE_BAR_INTERVAL: int = 60000
)->dict:
    '''
    :param candle: 历史K线数据
    :param interval: 间隔
    :param bar: 粒度
    :param MINUTE_BAR_INTERVAL: 每分钟的间隔单位(毫秒)
    :return:
        {
            'code' : True|False,    # True 验证成功 False 验证失败
            'data' : {},            # 空字典可忽略
            'msg'  : '...'          # 验证失败时记录失败原因
        }
    '''
    # 空数据
    if isnull(candle):
        return {'code': False, 'data': {}, 'msg': '[candle empty]'}
    # interval和bar不能同时为空
    if not interval and not bar:
        msg = 'Interval and bar cannot be None at the same time'
        raise exception.ParamException(func='valid_interval', msg=msg)
    # 优先级interval >> bar
    if pd.isnull(interval):
        interval = _interval.get_interval(bar=bar, MINUTE_BAR_INTERVAL=MINUTE_BAR_INTERVAL)
    # 时间间隔
    diffs = np.diff(candle[:, 0])
    if (diffs == interval).all():
        result = {'code': True, 'data': {}, 'msg': ''}
    else:
        diffs_unique = str((list(set(diffs.tolist()))))
        msg = '[valid candle interval error]: correct_interval={correct_interval} error_interval={error_interval}'.format(
            correct_interval=interval,
            error_interval=diffs_unique,
        )
        result = {'code': False, 'data': {}, 'msg': msg}
    return result


# 验证数据的起始时间
def valid_start(
        candle: np.array,
        start: Union[int, float, str, datetime.date],
        timezone: str = None
)->dict:
    '''
    :param candle: 历史K线数据
    :param start: 起点
        支持 毫秒级时间戳、日期格式字符串、日期类型与日期时间类型
    :param timezone: 时区
        {
            'code' : True|False,    # True 验证成功 False 验证失败
            'data' : {},            # 空字典可忽略
            'msg'  : '...'          # 验证失败时记录失败原因
        }
    '''
    if isnull(candle):
        result = {'code': False, 'data': {}, 'msg': '[candle empty]'}
        return result
    # 起始毫秒时间戳
    ts = _date.to_ts(date=start, timezone=timezone, default=np.nan)
    if candle[0, 0] == ts:
        result = {'code': True, 'data': {}, 'msg': ''}
    else:
        msg = '[valid candle start error]: correct_ts={correct_ts} error_ts={error_ts}'.format(
            correct_ts=str(start),
            error_ts=str(candle[0, 0]),
        )
        result = {'code': False, 'data': {}, 'msg': msg}
    return result


# 验证数据的终止时间
def valid_end(
        candle: np.array,
        end: Union[int, float, str, datetime.date],
        timezone: str = None
)->dict:
    '''
    :param candle: 历史K线数据
    :param start: 终点
        支持 毫秒级时间戳、日期格式字符串、日期类型与日期时间类型
    :param timezone: 时区
        {
            'code' : True|False,    # True 验证成功 False 验证失败
            'data' : {},            # 空字典可忽略
            'msg'  : '...'          # 验证失败时记录失败原因
        }
    '''
    # 终点毫秒时间戳
    if isnull(candle):
        result = {'code': False, 'data': {}, 'msg': '[candle empty]'}
        return result
    ts = _date.to_ts(date=end, timezone=timezone, default=np.nan)
    if candle[-1, 0] == ts:
        result = {'code': True, 'data': {}, 'msg': ''}
    else:
        msg = '[valid candle end error]: correct_ts={correct_ts} error_ts={error_ts}'.format(
            correct_ts=str(end),
            error_ts=str(candle[-1, 0]),
        )
        result = {'code': False, 'data': {}, 'msg': msg}
    return result


def valid_length(
        candle: np.array,
        length: int,
)->dict:
    '''
    :param candle: 历史K线数据
    :param length: 长度
            {
            'code' : True|False,    # True 验证成功 False 验证失败
            'data' : {},            # 空字典可忽略
            'msg'  : '...'          # 验证失败时记录失败原因
        }
    '''
    if isnull(candle):
        result = {'code': False, 'data': {}, 'msg': '[candle empty]'}
        return result
    if candle.shape[0] != length:
        result = {
            'code': False,
            'data': {},
            'msg': '[valid candle length error]: correct_length={correct_length} error_length={error_length}'.format(
                correct_length=length,
                error_length=candle.shape[0]
            )
        }
    else:
        result = {
            'code': True,
            'data': {},
            'msg': ''
        }
    return result
