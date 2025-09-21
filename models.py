from sqlalchemy import Column, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    is_subscriber = Column(Boolean, default=False)
    has_used_free_hq = Column(Boolean, default=False)
