from candlelite.exception._base import AbstractEXP, get_error_msg


class ExecuteException(AbstractEXP):
    def __init__(self, func, msg):
        self.error_msg = get_error_msg(func=func, reason=msg)
