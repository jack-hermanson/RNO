from functools import wraps

from flask import abort
from flask_login import current_user

from application.modules.accounts.ClearanceEnum import ClearanceEnum


def requires_clearance(minimum_clearance: ClearanceEnum):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.clearance >= minimum_clearance:
                return abort(403)
            return func(*args, **kwargs)

        return wrapped

    return decorator
