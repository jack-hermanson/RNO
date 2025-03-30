from application import db


# Many-to-many relationship
# role_account = db.Table(
#     "role_account",
#     db.Column("role_id", db.Integer, db.ForeignKey("role.role_id"), nullable=False, primary_key=True),
#     db.Column("account_id", db.Integer, db.ForeignKey("account.account_id"), nullable=False, primary_key=True),
# )
# todo - research other syntax/methods or stick with this if it's simpler


class Role(db.Model):
    # PK
    role_id = db.Column(db.Integer, primary_key=True)

    # What is this role called?
    name = db.Column(db.String(50), nullable=False)

    # Optional description of what this is.
    description = db.Column(db.String(255), nullable=True)

    # Is this an officer position, like President, VP, Secretary, Treasurer?
    is_officer = db.Column(db.Boolean, nullable=False)

    # Which accounts have this role?
    # accounts = db.relationship("Account", secondary=role_account, back_populates="roles")
