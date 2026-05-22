from models.user import db


class Order(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    total = db.Column(
        db.Integer
    )

    status = db.Column(
        db.String(100),
        default="Pending"
    )