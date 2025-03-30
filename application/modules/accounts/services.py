import time
from datetime import datetime

from flask import flash
from flask_login import login_user, current_user
from sqlalchemy import func

from application import bcrypt, db, logger
from .ClearanceEnum import ClearanceEnum
from .forms import CreateAccountForm, LoginForm, EditAccountForm
from .models import Account


def register(form: CreateAccountForm) -> Account:
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    account = Account()
    account.username = form.username.data.lower().strip()
    account.password = hashed_password
    account.email = form.email.data.lower().strip()
    account.clearance = ClearanceEnum.UNVERIFIED
    account.first_name = form.first_name.data.strip()
    account.last_name = form.last_name.data.strip()
    db.session.add(account)
    db.session.commit()
    return account


def get_edit_form() -> EditAccountForm:
    form = EditAccountForm()
    form.username.data = current_user.username
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    return form


def log_user_in(form: LoginForm) -> bool:
    account: Account = Account.query.filter(func.lower(Account.username) == func.lower(form.username.data)).first()
    if account and bcrypt.check_password_hash(account.password, form.password.data):
        login_user(account, remember=form.remember.data)
        last_login = account.last_login.strftime("%a %d %b %Y, %I:%M%p") if account.last_login is not None else "never"
        flash(f"Welcome back, {account.first_name}. Your last login was {last_login}.", "info")
        current_user.last_login = datetime.now()
        db.session.commit()
        return True
    else:
        time.sleep(2)  # prevent spamming
        logger.warn(f"Incorrect password for {form.username.data}")
        flash("Incorrect username or password.", "danger")
        return False


def edit_my_account(form: EditAccountForm):
    logger.debug(f"Editing current user's account {current_user.username}")
    account: Account = Account.query.filter(Account.account_id == current_user.account_id).first_or_404()
    if not account:
        raise ValueError("No account found. This should never happen.")

    # Uniqueness of username and email has already been checked.
    account.username = form.username.data.lower().strip()
    account.email = form.email.data.lower().strip()
    account.first_name = form.first_name.data.strip()
    account.last_name = form.last_name.data.strip()
    if form.password.data and form.confirm_password.data:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        account.password = hashed_password

    db.session.commit()
    flash("Account updated successfully.", "success")
    return True  # Success


def get_all_accounts() -> list[Account]:
    accounts: list[Account] = Account.query.order_by(Account.first_name).all()
    return accounts
