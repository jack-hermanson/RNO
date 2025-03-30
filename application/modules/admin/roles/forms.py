from flask_wtf import FlaskForm
from sqlalchemy import func, and_
from wtforms.fields import StringField, SubmitField, HiddenField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from application import logger
from application.modules.accounts.models import Account
from application.modules.admin.roles.models import Role


class CreateEditRoleForm(FlaskForm):
    role_id = HiddenField(validators=[Optional()])

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
        stripped_name = name.data.strip()
        if Role.query.filter(
            and_(
                func.lower(Role.name) == func.lower(stripped_name),
                form.role_id.data != "",
                Role.role_id != form.role_id.data,
            )
        ).all():
            raise ValidationError("That role has already been created.")
