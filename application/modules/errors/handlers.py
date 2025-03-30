import traceback

from flask import Blueprint, render_template, current_app
from werkzeug.exceptions import HTTPException

from application import logger

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def handle_http_exception(e):
    if current_app.debug:  # If debugging, re-raise the error to let Flask handle it
        raise e

    logger.debug("AN ERROR OCCURRED")
    logger.error(traceback.format_exc())

    status = 500
    if isinstance(e, HTTPException):
        status = e.code

    return render_template("errors/generic-error.html", status=status, error=str(e)), status
