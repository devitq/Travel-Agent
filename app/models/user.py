__all__ = ("User",)

import re
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

from app import session
from app.utils import geo
from app.utils.db import utcnow


Base: Any = declarative_base()


class User(Base):
    __tablename__ = "users"

    telegram_id = sa.Column(
        sa.BigInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        autoincrement=False,
    )
    username = sa.Column(sa.String(32), nullable=False, unique=True)
    age = sa.Column(sa.SmallInteger, nullable=False)
    bio = sa.Column(sa.String(100), nullable=True)
    sex = sa.Column(sa.String(6), nullable=True)
    country = sa.Column(sa.Text, nullable=False)
    city = sa.Column(sa.Text, nullable=False)
    date_joined = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=utcnow(),
    )

    @validates("username")
    def validate_username(self, key, value):
        regex_pattern = re.compile(r"^[a-zA-Z0-9_]{5,20}$")

        assert len(value) <= 32, "Username must be 32 characters or fewer."
        assert len(value) >= 5, "Username must be at least 5 characters."
        assert (
            re.match(regex_pattern, value) is not None
        ), "a-z, A-Z, 0-9, _ only allowed in username."

        if session.query(User).filter(User.username == value).first():
            raise AssertionError("Username is already taken.")

        return value

    @validates("age")
    def validate_age(self, key, value):
        assert str(value).isdigit(), "Invalid input. Please try again."
        value = int(value)
        assert value >= 13, "You must be at least 13 years old."
        assert value <= 120, "You must be less than 120 years old."

        return value

    @validates("bio")
    def validate_bio(self, key, value):
        if value is not None:
            assert len(value) <= 100, "Bio must be 100 characters or fewer."

        return value

    @validates("sex")
    def validate_sex(self, key, value):
        assert value in [
            "male",
            "female",
        ], "Invalid input. Please try again."

        return value

    @validates("country")
    def validate_country(self, key, value):
        verdict, normalized_value = geo.validate_country(
            value,
        )

        assert verdict, "There is no such country."

        return normalized_value

    def validate_city(self, city, country):
        verdict, normalized_value = geo.validate_city(
            city,
            country,
        )

        assert verdict, "There is no such city in selected country."

        return normalized_value

    def get_human_readable_datejoined(self):
        return self.date_joined.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_user_queryset_by_telegram_id(cls, telegram_id):
        return session.query(cls).filter(cls.telegram_id == telegram_id)

    @classmethod
    def get_user_by_telegram_id(cls, telegram_id):
        return (
            session.query(cls).filter(cls.telegram_id == telegram_id).first()
        )

    @classmethod
    def user_by_telegram_id_exist(cls, telegram_id):
        return (
            cls.get_user_by_telegram_id(
                telegram_id=telegram_id,
            )
            is not None
        )
