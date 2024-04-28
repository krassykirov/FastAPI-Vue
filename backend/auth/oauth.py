from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Form
from starlette.datastructures import URL
from typing import Union
from sqlmodel import Session, select
from starlette import status
from fastapi import Depends, HTTPException, APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db import get_session
import models
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import BackgroundTasks
from datetime import datetime, timedelta
from auth.oauth_schemas import OAuth2PasswordBearerCookie
from passlib.context import CryptContext
import datetime
from my_logger import detailed_logger

logger = detailed_logger()

pwd_context = CryptContext(schemes="bcrypt")

templates = Jinja2Templates(directory="static/templates")
oauth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/api/token")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    to_encode.update({"iat": datetime.datetime.utcnow()})
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire, 'iss': 'krassy'})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int, username: str, minutes: str):
    refresh_token_data = {"sub": username, 'user_id': user_id ,"iat": datetime.datetime.utcnow()}
    exp = datetime.datetime.utcnow() + timedelta(minutes=minutes)
    refresh_token_data.update({"exp": exp})
    refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized") # , headers = {"Location": "/login"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expires = payload.get("exp")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username, expires=expires)
    except jwt.ExpiredSignatureError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError as error:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    except Exception:
        raise credentials_exception
    query = select(models.User).where(models.User.username == token_data.username)
    user = db.exec(query).first()
    if user is None:
        raise credentials_exception
    return user

@oauth_router.post('/api/token/refresh', include_in_schema=True)
async def refresh_access_token(request: Request, db: Session = Depends(get_session)):
    try:
        data = await request.json()
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        try:
            data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
             raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError as error:
            raise HTTPException(status_code=401, detail=str(error))
        user_id = int(data.get("user_id"))
        user = db.exec(select(models.User).where(models.User.id == user_id)).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data={"sub": user.username, 'user_id': user.id, 'is_admin': user.is_admin}, expires_delta=access_token_expires)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@oauth_router.post('/api/token', include_in_schema=True)
async def login_access_token(*, request: Request, form_data: OAuth2PasswordRequestForm=Depends(),
                db: Session = Depends(get_session)):
    query = select(models.User).where(models.User.username == form_data.username)
    data = request.__dict__
    remember_me = [v.get('rememberMe') for k,v in data.items() if k == '_form' ][0]
    user = db.exec(query).first()
    if user and user.verify_password(form_data.password):
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if remember_me == 'true':
            access_token = create_access_token(
                data={"sub": user.username, 'user_id': user.id, 'is_admin': user.is_admin}, expires_delta=token_expires)
            refresh_token = create_refresh_token(user.id, user.username, minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 12)
            return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
        else:
            access_token = create_access_token(
            data={"sub": user.username, 'user_id': user.id, 'is_admin': user.is_admin}, expires_delta=token_expires)
            refresh_token = create_refresh_token(user.id, user.username, minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 5)
            return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Username or password are incorrect!")

@oauth_router.post("/signup", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def signup(request: Request, db: Session = Depends(get_session)):
    form_data = await request.form()
    username = form_data.get('username')
    passwd = form_data.get('password')
    passwd2 = form_data.get('password2')
    if (username and passwd and passwd2) and passwd == passwd2:
        query = select(models.User).where(models.User.username == username)
        user = db.exec(query).first()
        if user:
            logger.error(f"User with that name already exists!")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"This Email is taken. Try another")
        user = models.User(username=username)
        user.set_password(passwd)
        db.add(user)
        db.commit()
        logger.info(f'New user {user.username} has been created')
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Password did not match!")

@oauth_router.get("/login", include_in_schema=False)
def login(request: Request):
    response = templates.TemplateResponse("login.html",{"request":request})
    return response

@oauth_router.post('/token', include_in_schema=False)
def login_access_token_old(*, request: Request, response: Response, form_data: OAuth2PasswordRequestForm=Depends(),
                db: Session = Depends(get_session)):
    query = select(models.User).where(models.User.username == form_data.username)
    user = db.exec(query).first()
    if user and user.verify_password(form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response = RedirectResponse(url='/admin', status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response

    else:
        context = {'request': request, 'message': "Username or password are incorrect!"}
        print('failed response login:', r)
        return templates.TemplateResponse("login.html", context)

# @oauth_router.get("/signup", include_in_schema=False)
# def login(request: Request):
#     response = templates.TemplateResponse("signup.html",{"request":request})
#     return response

# @oauth_router.get("/logout", include_in_schema=False)
# def logout(request: Request):
#     response = RedirectResponse("login.html", status_code=status.HTTP_302_FOUND)
#     response = templates.TemplateResponse("login.html",{"request":request, 'current_user': None})
#     response.delete_cookie(key="access_token")
#     return response
