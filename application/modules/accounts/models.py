from application import db
from flask_login import UserMixin

from application.modules.accounts.ClearanceEnum import ClearanceEnum


class Account(db.Model, UserMixin):
    def get_id(self):
        return self.account_id

    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String, nullable=False)
    clearance = db.Column(db.Integer, default=ClearanceEnum.UNVERIFIED, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
