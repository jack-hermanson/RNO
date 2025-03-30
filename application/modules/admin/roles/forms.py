from flask_wtf import FlaskForm
from sqlalchemy import func, and_, or_
from wtforms.fields import StringField, SubmitField, HiddenField, IntegerField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from wtforms.widgets.core import HiddenInput

from application import logger
from application.modules.accounts.models import Account
from application.modules.admin.roles.models import Role


class CreateEditRoleForm(FlaskForm):
    role_id = IntegerField(validators=[Optional()], widget=HiddenInput())

    name = StringField(
        "Name",
        validators=[DataRequired(), Length(1, 50)],
        render_kw={"autofocus": "true"},
        description='The name of this role, like "Vice President".',
    )

    description = StringField(
        "Description",
        validators=[Length(2, 255), Optional()],
        description="Optional, short description of what this role is or does.",
    )

    is_officer = BooleanField(
        "Officer", validators=[], description="Officer position like President, Vice President, Treasurer, Secretary."
    )

    submit = SubmitField("Create" if role_id is None else "Save Changes")

    @staticmethod
    def validate_name(form, name):

        # stripped_name = name.data.strip()
        existing_role = Role.query.filter(func.lower(Role.name) == func.lower(func.trim(name.data))).first()
        if existing_role and form.role_id.data != existing_role.role_id:
            raise ValidationError("That role has already been created.")
