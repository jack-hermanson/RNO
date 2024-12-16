from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email

from application.modules.accounts.models import Account

username_length = Length(min=2, max=24)
first_name_length = Length(min=2, max=16)
last_name_length = Length(min=2, max=24)
password_length = Length(max=100)
email_length = Length(min=5, max=42)


class CreateOrEditFormBase(FlaskForm):
    """Just the base - inherit this in create and edit"""

    first_name = StringField(
        "First Name",
        filters=[lambda x: x.strip() if x else x],
        validators=[DataRequired(), first_name_length],
        render_kw={
            "autofocus": "true",
            "spellcheck": "false",
            "autocorrect": "off",
        },
    )
    last_name = StringField(
        "Last Name",
        filters=[lambda x: x.strip() if x else x],
        validators=[DataRequired(), last_name_length],
        render_kw={"spellcheck": "false", "autocorrect": "off"},
    )
    email = StringField(
        "Email",
        filters=[lambda x: x.strip() if x else x],
        validators=[Email()],
        render_kw={
            "spellcheck": "false",
            "autocorrect": "off",
            "autocapitalize": "off",
        },
        description="Your email address to be used for notifications and password resets.",
    )
    username = StringField(
        "Username",
        filters=[lambda x: x.strip() if x else x],
        validators=[DataRequired(), username_length],
        description="A unique username to you that you can remember. This is not displayed to others.",
        render_kw={
            "spellcheck": "false",
            "autocorrect": "off",
            "autocomplete": "off",
            "autocapitalize": "off",
        },
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[lambda x: x.strip() if x else x],
        validators=[DataRequired(), username_length],
        description="Your unique username.",
        render_kw={
            "autofocus": "true",
            "spellcheck": "false",
            "autocorrect": "off",
            "autocapitalize": "off",
        },
    )
    password = PasswordField("Password", validators=[DataRequired(), password_length], render_kw={})
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Log In")

    # @staticmethod
    # def validate_username(_, username):
    #     if not Account.query.filter(func.lower(Account.username) == func.lower(username.data)).count():
    #         raise ValidationError("Doesn't exist.")


class CreateAccountForm(CreateOrEditFormBase):
    password = PasswordField(
        "Password",
        validators=[DataRequired(), password_length],
        description="Make this something you can remember (or even better—use a password manager so you don't have to "
        "remember it).",
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", "Your passwords must match.")],
        description="Type in your password again to confirm it's correct.",
    )
    submit = SubmitField("Create Account")

    @staticmethod
    def validate_username(_, username):
        stripped_username = username.data.strip()
        if Account.query.filter(func.lower(Account.username) == func.lower(stripped_username)).all():
            raise ValidationError("That username has already been taken.")

    @staticmethod
    def validate_email(_, email):
        stripped_email = email.data.strip()
        if Account.query.filter(func.lower(Account.email) == func.lower(stripped_email)).all():
            raise ValidationError("That email has already been used.")


# if we allowed editing name, then CreateOrEditFormBase will be used, until then don't inherit
# class EditAccountForm(CreateOrEditFormBase):
class EditAccountForm(FlaskForm):
    password = PasswordField("Password", validators=[password_length])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password", "Your passwords must match.")])
    submit = SubmitField("Save Changes")

    @staticmethod
    def validate_password(_, password):
        if len(password.data) > password_length.max:
            raise ValidationError(f"Name must be fewer than {password_length.max} characters")
