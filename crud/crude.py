from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..sql_app import model, schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, email: str) -> model.User:
    return db.query(model.User).filter(model.User.email == email).first()


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.LoginUserSchema):
    hashed_password = pwd_context.hash(user.password)
    db_user = model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def update_profile(db: Session, profile: schema.ProfileSchema, user_email: str):
    user_profile = model.Profile(**profile.dict(), user=user_email)
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    return user_profile


def search(db: Session, text:str=None, max_follower: int=None, min_follower: int=None):
    if text:
        return db.query(model.Profile).filter((model.Profile.username.like(f'%{text}%')) | (model.Profile.bio.like(f'%{text}%'))).all()
    elif min_follower:
        return db.query(model.Profile).filter(model.Profile.followers >= min_follower).all()

    return db.query(model.Profile).filter(model.Profile.followers < max_follower).all()



def login_user(db:Session, user: schema.LoginUserSchema) -> bool:
    stored_user = get_user(db, user.email)
    return pwd_context.verify(user.password, stored_user.hashed_pass)