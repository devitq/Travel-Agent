# flake8: noqa

from app.models.base import Base
import app.models.user
import app.models.travel

Base.registry.configure()
