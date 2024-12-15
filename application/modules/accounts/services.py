import time
from datetime import datetime

from flask import request, flash
from flask_login import login_user, current_user
from sqlalchemy import func

from .ClearanceEnum import ClearanceEnum
from .forms import CreateAccountForm, LoginForm
from .models import Account
from application import bcrypt, db, logger


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


def log_user_in(form: LoginForm) -> bool:
    user: Account = Account.query.filter(func.lower(Account.username) == func.lower(form.username.data)).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        last_login = user.last_login.strftime("%a %d %b %Y, %I:%M%p") if user.last_login is not None else "never"
        flash(f"Welcome back, {user.first_name}. Your last login was {last_login}.", "info")
        current_user.last_login = datetime.now()
        db.session.commit()
        return True
    else:
        time.sleep(2)  # prevent spamming
        logger.warn(f"Incorrect password for {form.username.data}")
        flash("Incorrect username or password.", "danger")
        return False
