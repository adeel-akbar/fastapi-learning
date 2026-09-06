from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key = True, nullable = False)
    title: Mapped[str] = mapped_column(nullable = False)
    author: Mapped[str] = mapped_column(nullable = False)
    published: Mapped[bool] = mapped_column(server_default = "true", 
                    nullable = False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True), 
        nullable = False, server_default = func.now())