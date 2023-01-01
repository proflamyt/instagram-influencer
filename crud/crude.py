from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sql_app import model, schema
from pydantic import EmailStr 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, email: str) -> model.User:
    return db.query(model.User).filter(model.User.email == email).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).order_by(model.User.time_created).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.LoginUserSchema):
    hashed_password = pwd_context.hash(user.password)
    db_user = model.User(email=user.email, hashed_pass=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def update_profile(db: Session, profile: schema.ProfileSchema, user_email: EmailStr ):
    user = get_user_by_email(db, user_email)
    if user is None:
        return None
    user_profile = model.Profile(**profile.dict())
    user.profile = user_profile
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        'email': user.email,
        **user.profile.__dict__
        
    }


def search(db: Session, text:str=None, max_follower: int=None, min_follower: int=None):
    if text:
        return db.query(model.Profile).filter((model.Profile.username.like(f'%{text}%')) | (model.Profile.bio.like(f'%{text}%'))).all()
    elif min_follower:
        return db.query(model.Profile).filter(model.Profile.follower_count >= min_follower).all()

    return db.query(model.Profile).filter(model.Profile.follower_count < max_follower).all()



def login_user(db:Session, user: schema.LoginUserSchema) -> model.User | None:
    stored_user = get_user(db, user.email)
    if stored_user and pwd_context.verify(user.password, stored_user.hashed_pass):
        return stored_user
    return None