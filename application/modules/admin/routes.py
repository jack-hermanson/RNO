from functools import wraps

from flask import Blueprint, abort, render_template
from flask_login import login_required, current_user

from application.modules.accounts.ClearanceEnum import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def dashboard():
    return render_template("admin/dashboard.html")
