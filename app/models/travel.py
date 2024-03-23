__all__ = ("Travel", "Location")

import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates

from app import messages, session
from app.models import Base
from app.models.user import User


association_table = sa.Table(
    "user_travel_association",
    Base.metadata,
    sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.telegram_id")),
    sa.Column("travel_id", sa.Integer, sa.ForeignKey("travels.id")),
)


class Travel(Base):
    __tablename__ = "travels"

    id = sa.Column(  # noqa: A003
        sa.Integer,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        index=True,
    )
    title = sa.Column(
        sa.String(50),
        nullable=False,
        unique=True,
    )
    description = sa.Column(
        sa.String(100),
        nullable=True,
    )

    author_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey(User.telegram_id),
        nullable=False,
    )

    users = relationship(
        User,
        secondary=association_table,
        backref="travels",
    )

    locations = relationship("Location", backref="travel")
    notes = relationship("Note", backref="travel")

    @validates("title")
    def validate_title(self, key, value):
        assert len(value) <= 30, "Title must be 30 characters or fewer."
        assert "👑" not in value, "👑 is not allowed symbol."

        if session.query(Travel).filter(Travel.title == value).first():
            raise AssertionError("This title is already taken.")

        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is not None:
            assert (
                len(value) <= 100
            ), "Description must be 100 characters or fewer."

        return value

    def get_travel_text(self):
        return messages.TRAVEL_DETAIL.format(
            title=self.title,
            description=self.description,
        )

    @classmethod
    def get_travel_by_id(cls, travel_id):
        return session.query(Travel).filter(Travel.id == travel_id).first()


class Location(Base):
    __tablename__ = "locations"

    id = sa.Column(  # noqa: A003
        sa.Integer,
        unique=True,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name = sa.Column(sa.Text, nullable=False)
    date_start = sa.Column(sa.Date(), nullable=False)
    date_end = sa.Column(sa.Date(), nullable=False)

    travel_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("travels.id"),
        nullable=False,
    )


class Note(Base):
    __tablename__ = "notes"

    id = sa.Column(  # noqa: A003
        sa.Integer,
        unique=True,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    file_id = sa.Column(sa.Text, nullable=False)
    file_name = sa.Column(sa.Text, nullable=False)
    file_type = sa.Column(sa.Text, nullable=False)
    public: sa.Column[bool] = sa.Column(
        sa.Boolean(),
        nullable=False,
        default=False,
    )

    author_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey(User.telegram_id),
        nullable=False,
    )
    travel_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("travels.id"),
        nullable=False,
    )
