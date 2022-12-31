from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pyjwt import decode, encode



def get_current_user(token: str = Depends(get_token)):
    try:
        payload = decode(token, secret, algorithms=[ALGORITHM])
        return User(**payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_token(authorization: HTTPAuthorizationCredentials = Depends(get_authorization)):
    if authorization.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.credentials

def get_authorization(authorization: str = Depends(get_api_key)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return HTTPAuthorizationCredentials(scheme=authorization.split(" ", 1)[0], credentials=authorization.split(" ", 1)[1])

def get_api_key(api_key: str = Header(...)):
    return api_key

# @app.get("/users/me")
# def read_current_user(current_user: User = Depends(get_current_user)):
#     return current_user
