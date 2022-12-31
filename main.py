from crud.crude import get_user
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
from sql_app.model import User as UserModel
import datetime
from sql_app.schema import CreateUserSchema, LoginUserSchema, UserBaseSchema, UserResponse
from sql_app.database import Base, SessionLocal, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/login', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def login_user(payload: CreateUserSchema, request: Request):
    
    return {
        'payload': payload
    }
  
@app.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    user_email = payload.email.lower()
    if get_user(db, user_email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hash =  payload.password
    user =  UserModel(email=user_email, hashed_pass=hash, time_created=datetime.utcnow())
    db.session.add(user)
    db.session.commit()

    
    return {
        'payload': user
    }
  
# authenticated route
@app.post('/user/update', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def update_user(payload: UserBaseSchema, request: Request):
    user = UserModel()
    db.session.update(user)
    db.session.commit()
    ...


