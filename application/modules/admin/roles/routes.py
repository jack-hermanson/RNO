from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_required

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.utils.CrudEnum import CrudEnum
from .forms import CreateEditRoleForm
from .services import get_roles, create_new_role, delete_role, prefill_edit_role_form_values, edit_role

roles = Blueprint("roles", __name__, url_prefix="/admin/roles")


@roles.route("/")
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def index():
    roles_list = get_roles()
    return render_template("admin/roles/index.html", title="Roles", roles_list=roles_list)


@roles.route("/create", methods=["GET", "POST"])
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def create():
    form = CreateEditRoleForm()
    if form.validate_on_submit():
        role = create_new_role(form)
        flash(f"Role {role.name} created successfully.", "success")
        return redirect(url_for("roles.index"))

    return render_template("admin/roles/create_edit.html", form=form, mode=CrudEnum.CREATE, title="Create Role")


@roles.route("/delete/<int:role_id>", methods=["POST"])
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def delete(role_id: int):
    delete_role(role_id)
    flash("Role deleted successfully.", "success")
    return redirect(url_for("roles.index"))


@roles.route("/edit/<int:role_id>", methods=["GET", "POST"])
@login_required
@requires_clearance(ClearanceEnum.ADMIN)
def edit(role_id: int):
    form = CreateEditRoleForm()
    if form.validate_on_submit():
        edit_role(form)
        flash("Role edited successfully.", "success")
        return redirect(url_for("roles.index"))
    elif request.method == "GET":
        prefill_edit_role_form_values(form, role_id)
    return render_template("admin/roles/create_edit.html", form=form, mode=CrudEnum.EDIT, title=f"Edit Role")
