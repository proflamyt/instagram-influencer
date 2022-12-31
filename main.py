from datetime import timedelta
from auth import create_access_token, get_current_user
from crud import crude
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sql_app.schema import CreateUserSchema, LoginUserSchema, ProfileSchema, UserResponse
from sql_app.database import Base, SessionLocal, engine
from config import settings


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
async def login_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    user = crude.login_user(db, payload)
    if user:
        # sign jwt
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
        access_token = create_access_token(
            data= {"sub": user.email},
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"

        }
    raise HTTPException(status_code=400, detail="Email already registered")
  
@app.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    
    if crude.get_user(db, payload.email.lower()):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crude.create_user(db, payload)

    return {
        'payload': user
    }
  
# authenticated route Depends
@app.post('/user/update', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def update_user(payload: ProfileSchema, db: Session = Depends(get_db), current_user_email: str= Depends(get_current_user)):
    user = crude.update_profile(db, payload, current_user_email)
    return user



@app.get('/search', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def get_users(text:str=None, max_follower: int =None, min_follower: int=None, db: Session = Depends(get_db)):
    if text or max_follower or min_follower:
        return crude.search(text, max_follower, min_follower) 
    return crude.get_users(db)