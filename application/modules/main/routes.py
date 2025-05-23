from flask import Blueprint, render_template
from application import logger

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index():
    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    return render_template("main/index.html")
