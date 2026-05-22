import os

BASE_DIR = "/tmp"


class Config:

    SECRET_KEY = "secret123"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "ecommerce.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False