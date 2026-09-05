from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func

from .database import Base


# this will create a table in the database named posts.
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())