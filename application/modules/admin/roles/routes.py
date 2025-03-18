from flask import Blueprint
from flask_login import login_required

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance

roles = Blueprint("roles", __name__, url_prefix="/admin/roles")


@roles.route("/")
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def index():
    pass
