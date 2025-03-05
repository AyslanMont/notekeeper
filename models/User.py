from notekeeper.database.config import Base, db_session
from notekeeper.models.Note import Note
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    notes:Mapped[List['Note']] = relationship("Note", backref="user")
    passwd: Mapped[str] = mapped_column(String(255), nullable=False)

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd = passwd

    def save(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def get(cls, id):
        return db_session.get(cls, id)

    @classmethod
    def get_by_email(cls, email):
        return db_session.query(cls).filter_by(email=email).first()