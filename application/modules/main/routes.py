from flask import Blueprint, render_template

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index():
    return render_template("main/index.html")
