__all__ = ("Travel", "Location")

import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates

from app import messages, session
from app.models import Base
from app.models.user import User
from app.utils.geo import get_location_by_name


association_table = sa.Table(
    "user_travel_association",
    Base.metadata,
    sa.Column(
        "user_id",
        sa.BigInteger,
        sa.ForeignKey("users.telegram_id", ondelete="CASCADE"),
    ),
    sa.Column(
        "travel_id",
        sa.Integer,
        sa.ForeignKey("travels.id", ondelete="CASCADE"),
    ),
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
        sa.ForeignKey(User.telegram_id, ondelete="CASCADE"),
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
            travel_id=self.id,
            title=self.title,
            description=(
                self.description if self.description else messages.NOT_SET
            ),
        )

    @classmethod
    def get_notes(cls, author_id, travel, public=True):
        return (
            session.query(Note)
            .filter(
                Note.author_id == author_id,
                Note.travel_id == travel.id,
                Note.public == public,
            )
            .all()
        )

    @classmethod
    def get_travel_by_id(cls, travel_id):
        return session.query(Travel).filter(Travel.id == travel_id).first()

    @classmethod
    def get_travel_queryset_by_id(cls, travel_id):
        return session.query(Travel).filter(Travel.id == travel_id)

    @classmethod
    def get_sorted_locations(cls, travel, asc=True):
        return sorted(
            travel.locations,
            key=lambda location: location.date_end,
            reverse=asc,
        )


class Location(Base):
    __tablename__ = "locations"

    id = sa.Column(  # noqa: A003
        sa.Integer,
        unique=True,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    location = sa.Column(sa.Text, nullable=False)
    date_start = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
    )
    date_end = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
    )

    travel_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("travels.id", ondelete="CASCADE"),
        nullable=False,
    )

    def validate_location(self, key, value):
        geocode = get_location_by_name(value)

        assert geocode[0], "Invalid location."

        return geocode[1].raw["display_name"]

    def validate_date_start(self, key, value):
        try:
            value_datetime = datetime.datetime.strptime(
                value,
                "%Y-%m-%d %H:%M",
            )
            value_datetime = value_datetime.replace(tzinfo=datetime.UTC)
        except ValueError:
            raise AssertionError("Invalid datetime format.")

        assert value_datetime >= datetime.datetime.now(
            datetime.UTC,
        ), "Invalid datetime."

        return value_datetime

    def validate_date_end(self, key, value):
        try:
            value_datetime = datetime.datetime.strptime(
                value,
                "%Y-%m-%d %H:%M",
            )
            value_datetime = value_datetime.replace(tzinfo=datetime.UTC)
        except ValueError:
            raise AssertionError("Invalid datetime format.")

        assert value_datetime >= datetime.datetime.now(
            datetime.UTC,
        ), "Invalid datetime."

        return value_datetime

    def get_location_text(self):
        return messages.LOCATION_DETAIL.format(
            location=self.location,
            date_start=datetime.datetime.strftime(
                self.date_start,
                "%Y-%m-%d %H:%M",
            ),
            date_end=datetime.datetime.strftime(
                self.date_end,
                "%Y-%m-%d %H:%M",
            ),
        )

    @classmethod
    def get_location_by_id(cls, location_id):
        return (
            session.query(Location).filter(Location.id == location_id).first()
        )

    @classmethod
    def get_location_queryset_by_id(cls, location_id):
        return session.query(Location).filter(Location.id == location_id)


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
        sa.ForeignKey(User.telegram_id, ondelete="CASCADE"),
        nullable=False,
    )
    travel_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("travels.id", ondelete="CASCADE"),
        nullable=False,
    )

    def get_note_text(self):
        return messages.NOTE_DETAIL.format(
            file_name=self.file_name,
            file_type=self.file_type.capitalize(),
            public="Yes" if self.public else "No",
        )

    @classmethod
    def get_note_by_id(cls, note_id):
        return session.query(Note).filter(Note.id == note_id).first()

    @classmethod
    def get_note_queryset_by_id(cls, note_id):
        return session.query(Note).filter(Note.id == note_id)
