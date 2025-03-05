from notekeeper.database.config import Base, db_session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

class Note(Base):
    __tablename__ = 'notes'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    text:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
    
    def save(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def get_by_user(cls, user_id):
        return db_session.query(cls).filter_by(user_id=user_id).all()
