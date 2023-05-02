from candlelite.exception._base import AbstractEXP


class CandleFileNotExist(AbstractEXP):
    def __init__(
            self,
            symbol: str,
            date: str = None,
            path: str = None,
    ):
        self.error_msg = 'symbol={symbol:<10} date={date} path={path}'.format(
            symbol=str(symbol),
            date=str(date),
            path=str(path),
        )


class CandleIntervalError(AbstractEXP):
    def __init__(
            self,
            symbol: str,
            msg: str,
    ):
        self.error_msg = 'symbol={symbol:<10} msg={msg}'.format(
            symbol=str(symbol),
            msg=str(msg)
        )


class CandleStartError(AbstractEXP):
    def __init__(
            self,
            symbol: str,
            msg: str,
    ):
        self.error_msg = 'symbol={symbol:<10} msg={msg}'.format(
            symbol=str(symbol),
            msg=str(msg)
        )


class CandleEndError(AbstractEXP):

    def __init__(
            self,
            symbol: str,
            msg: str,
    ):
        self.error_msg = 'symbol={symbol:<10} msg={msg}'.format(
            symbol=str(symbol),
            msg=str(msg)
        )


class CandleDatesNonError(AbstractEXP):
    def __init__(self, error_msg):
        self.error_msg = error_msg
