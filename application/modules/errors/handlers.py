import traceback

from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

from application import logger

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
def handle_http_exception(e):
    logger.debug("AN ERROR OCCURRED")
    logger.error(traceback.format_exc())
    status = e.get_response().status_code
    return render_template("errors/generic-error.html", status=status, error=e.__str__()), status


@errors.app_errorhandler(Exception)
def handle_generic_exception(e):
    logger.debug("AN ERROR OCCURRED")
    logger.error(traceback.format_exc())
    status = 500
    return render_template("errors/generic-error.html", status=status, error=e.__str__()), status


# @errors.app_errorhandler(403)
# def error_403(error):
#     return render_template("errors/generic-error.html", error=error, status=403), 403
