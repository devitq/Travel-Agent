from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.config import Config

engine: Engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
