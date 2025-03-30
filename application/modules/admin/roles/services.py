from application import db, logger
from application.modules.accounts.services import get_all_accounts
from application.modules.admin.roles.forms import CreateEditRoleForm
from application.modules.admin.roles.models import Role
from flask_login import current_user


def get_roles() -> list[Role]:
    return Role.query.order_by(Role.name).all()


def get_role(role_id: int):
    return Role.query.get_or_404(role_id)


def get_role_account_choices():
    options = [
        (option.account_id, f"{option.first_name} {option.last_name} ({option.username})")
        for option in get_all_accounts()
    ]
    options.insert(0, (None, ""))
    return options


def create_new_role(form: CreateEditRoleForm):
    logger.debug("Creating new role")
    new_role = Role()
    new_role.name = form.name.data.strip()
    new_role.description = form.description.data.strip()
    new_role.is_officer = form.is_officer.data
    db.session.add(new_role)
    db.session.commit()
    return new_role


def edit_role(form: CreateEditRoleForm):
    logger.debug(f"Editing role {form.role_id.data}")
    role = Role.query.get_or_404(form.role_id.data)
    _set_role_from_form(form, role)
    db.session.commit()


def prefill_edit_role_form_values(form: CreateEditRoleForm, role_id: int):
    role = Role.query.get_or_404(role_id)
    form.name.data = role.name
    form.description.data = role.description
    form.is_officer.data = role.is_officer
    form.role_id.data = role.role_id


def _set_role_from_form(form: CreateEditRoleForm, role: Role):
    role.name = form.name.data.strip()
    role.description = form.description.data
    role.is_officer = form.is_officer.data
    return role


def delete_role(role_id: int):
    logger.info(f"{current_user.username} is deleting role {role_id}")
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
