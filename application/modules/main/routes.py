from flask import Blueprint

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index():
    return "yeva", 200
