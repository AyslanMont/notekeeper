from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine('sqlite:///notekeeper.db')
db_session = Session(bind=engine)

class Base(DeclarativeBase):
    pass