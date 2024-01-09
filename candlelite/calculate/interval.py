import numpy as np
from candlelite import exception

__all__ = ['get_interval', 'predict_interval']


# 获取时间粒度的数字间隔（默认毫秒）
def get_interval(bar: str, MINUTE_BAR_INTERVAL=60000) -> float:
    '''
    :param bar: 时间粒度 1m 3m 5m 15m 1h 2h 4h 1d ...
    :param MINUTE_BAR_INTERVAL: 每分钟的数字间隔，默认毫秒
    '''
    bar_int = int(bar[0:-1].strip())
    suffix = bar[-1].lower()
    if suffix == 's':
        interval = int((MINUTE_BAR_INTERVAL / 60) * bar_int)
    elif suffix == 'm':
        interval = MINUTE_BAR_INTERVAL * bar_int
    elif suffix == 'h':
        interval = MINUTE_BAR_INTERVAL * 60 * bar_int
    elif suffix == 'd':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * bar_int
    elif suffix == 'w':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * 7 * bar_int
    else:
        raise exception.ParamBarException(
            func='get_interval',
            bar=bar
        )
    return interval


# 预计历史K线的时间间隔
def predict_interval(candle: np.array) -> float:
    '''
    :param candle: 历史K线
    '''
    return np.min(np.diff(candle[:, 0]))
