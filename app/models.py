import datetime
from .database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default = text('true'), nullable=False)

    # POSTGRES specific - postgres accepts TRUE as boolean,but not all databases do
    # published = Column(Boolean, server_default = 'TRUE', nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))