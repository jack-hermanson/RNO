from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_required

from application import login_manager, bcrypt, db
from application.modules.accounts.forms import LoginForm, CreateAccountForm, EditAccountForm
from application.modules.accounts.models import Account
from . import services

accounts = Blueprint("accounts", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


@accounts.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit() and services.log_user_in(form):
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.index"))

    return render_template("accounts/login.html", form=form)


@accounts.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("You are not logged in, so you cannot log out!", "danger")
        return redirect(url_for("accounts.login"))

    name = current_user.username
    logout_user()
    flash(f"Goodbye, {name}.", "info")
    return redirect(url_for("main.index"))


@accounts.route("/register", methods=["GET", "POST"])
def register():
    form = CreateAccountForm()
    if form.validate_on_submit():
        created_account = services.register(form)
        flash(f'Account "{created_account.username}" registered successfully. Please log in.', "success")
        return redirect(url_for("accounts.login"))
    return render_template("accounts/register.html", form=form)


@accounts.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditAccountForm()
    if form.validate_on_submit() and services.edit_my_account(form):
        return redirect(url_for("accounts.edit"))
    elif request.method == "GET":
        form = services.get_edit_form()

    return render_template("accounts/edit.html", form=form)


@accounts.route("/me")
@login_required
def me():
    return render_template("accounts/me.html", title=f"{current_user.first_name} {current_user.last_name}")


@accounts.route("/change-password", methods=["POST"])
@login_required
def change_password():
    form = EditAccountForm()
    if form.validate_on_submit():
        account = Account.query.get_or_404(current_user.account_id)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        account.password = hashed_password
        db.session.commit()
        flash("Password changed successfully.", "success")
    return render_template("accounts/edit.html", form=form)
