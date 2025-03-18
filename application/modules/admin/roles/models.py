from application import db


class Role(db.Model):
    # PK
    role_id = db.Column(db.Integer, primary_key=True)

    # What is this role called?
    name = db.Column(db.String(50), nullable=False)

    # Optional description of what this is.
    description = db.Column(db.String(255), nullable=True)

    # Is this an officer position, like President, VP, Secretary, Treasurer?
    is_officer = db.Column(db.Boolean, nullable=False)
