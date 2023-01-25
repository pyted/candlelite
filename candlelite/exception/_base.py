class AbstractEXP(Exception):
    error_msg: str

    def __str__(self):
        return self.error_msg

def get_error_msg(func,reason):
    msg = '[ERROR] [{func}] {reason}'.format(
        func= func,reason=reason
    )
    return msg