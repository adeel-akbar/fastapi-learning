from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key= True, nullable= False)
    title: Mapped[str] = mapped_column(nullable= False)
    content: Mapped[str] = mapped_column(nullable= False)
    published: Mapped[bool] = mapped_column(nullable= False, server_default= "true")
    created_at: Mapped[datetime]= mapped_column(TIMESTAMP(timezone= True),
                server_default= func.now(), nullable= False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True, nullable = False)
    email: Mapped[str] = mapped_column(nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True), 
                    server_default = func.now(), nullable = False)