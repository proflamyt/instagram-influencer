from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_pass = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    bio = Column(String(100))
    follower_count = Column(Integer)
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    

Profile.user = relationship("User", back_populates="profile", uselist=False)