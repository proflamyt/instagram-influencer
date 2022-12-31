from sqlalchemy.orm import Session

from ..sql_app import model, schema


def get_user(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.LoginUserSchema):
    hashed_password = user.password + "notreallyhashed"
    db_user = model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def update_profile(db: Session, profile: schema.ProfileSchema, user_id: int):
    user_profile = model.Profile(**profile.dict(), user=user_id)
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