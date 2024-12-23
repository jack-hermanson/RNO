from functools import wraps
from http import HTTPStatus

from flask import abort, request
from flask_login import current_user

from application import logger
from application.modules.accounts.ClearanceEnum import ClearanceEnum


def requires_clearance(minimum_clearance: ClearanceEnum):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.clearance >= minimum_clearance:
                logger.warn(f"<{current_user.username}, {current_user.account_id}> tried to access {request.path}")
                return abort(HTTPStatus.FORBIDDEN)
            return func(*args, **kwargs)

        return wrapped

    return decorator
