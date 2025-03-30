import traceback

from flask import Blueprint, render_template, request, make_response
from werkzeug.exceptions import HTTPException

from application import logger

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
@errors.app_errorhandler(Exception)
def handle_exception(e):
    logger.error(traceback.format_exc())
    status = e.get_response().status_code
    return render_template("errors/generic-error.html", status=status, error=e.__str__()), status


# @errors.app_errorhandler(403)
# def error_403(error):
#     return render_template("errors/generic-error.html", error=error, status=403), 403
