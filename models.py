from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Avatar(Base):
    __tablename__ = "avatars"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    file_path = Column(String)

class Garment(Base):
    __tablename__ = "garments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    file_path = Column(String)
