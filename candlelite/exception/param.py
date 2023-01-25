from candlelite.exception._base import AbstractEXP, get_error_msg


class ParamException(AbstractEXP):
    def __init__(self, func, msg):
        self.error_msg = get_error_msg(func=func, reason=msg)


class ParamBarException(AbstractEXP):
    def __init__(self, func, bar, pmt="bar must like ['1m','3m','5m','30m','1h','2h','4h','6h','1d'...]"):
        reason = 'bar={bar}\n{pmt}'.format(
            bar=str(bar),
            pmt=pmt,
        )
        self.error_msg = get_error_msg(func=func, reason=reason)


class PosSideException(AbstractEXP):
    def __init__(self, func, posSide, pmt="posSide must in ['LONG','SHORT']"):
        reason = 'posSide={posSide}\n{pmt}'.format(
            posSide=str(posSide),
            pmt=pmt,
        )
        self.error_msg = get_error_msg(func=func, reason=reason)
