from crud import crude
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sql_app.schema import CreateUserSchema, LoginUserSchema, ProfileSchema, UserBaseSchema, UserResponse
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
async def login_user(payload: CreateUserSchema):
    
    return {
        'payload': payload
    }
  
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
async def update_user(payload: ProfileSchema, db: Session = Depends(get_db)):
    user = crude.update_profile(user_id, payload)
    return user



@app.get('/search', status_code=status.HTTP_201_CREATED, response_model=UserBaseSchema)
async def get_users(text:str=None, max_follower: int =None, min_follower: int=None, db: Session = Depends(get_db)):
    if text or max_follower or min_follower:
        return crude.search(text, max_follower, min_follower) 
    return crude.get_users(db)