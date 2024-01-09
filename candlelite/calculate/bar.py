import numpy as np
from candlelite import exception

__all__ = ['predict_bar']


# 估计K线的时间粒度
def predict_bar(candle: np.array, MINUTE_BAR_INTERVAL=60000) -> str:
    '''
    :param candle: 历史K线
    :param MINUTE_BAR_INTERVAL: 每分钟的时间间隔，默认单位毫秒

    支持的时间粒度估计: 秒s 分钟m 小时h 天d
    '''
    bar_interval = np.min(np.diff(candle[:, 0]))
    bar_int = bar_interval / MINUTE_BAR_INTERVAL
    if bar_int < 1:
        bar_int = bar_interval / (MINUTE_BAR_INTERVAL / 60)
        suffix = 's'
    elif bar_int <= 59:
        suffix = 'm'
        bar_int = bar_int
    elif bar_int <= 60 * 23:
        suffix = 'h'
        bar_int = bar_int / 60
    else:
        bar_int = bar_int / (60 * 24)
        suffix = 'd'

    if not bar_int == int(bar_int):
        raise exception.ExecuteException(
            func='predict_bar',
            msg='The predict bar result is {bar_int}{suffix}'.format(
                bar_int=str(bar_int),
                suffix=suffix,
            )
        )
    return '{bar_int}{suffix}'.format(bar_int=int(bar_int), suffix=suffix)


if __name__ == '__main__':
    pass
