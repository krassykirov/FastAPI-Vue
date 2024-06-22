from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from fastapi import APIRouter, Depends, Request, Security
from typing import Union
from sqlmodel import Session, select
from starlette import status
from fastapi import Depends, HTTPException, APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db.database_factory import get_session
import models
from jose import JWTError, jwt, jws
from datetime import datetime, timedelta
from auth.oauth_schemas import OAuth2PasswordBearerCookie
from passlib.context import CryptContext
from my_logger import detailed_logger
import datetime, uuid
import urllib.parse, requests, json
import adal, os
from dotenv import load_dotenv

load_dotenv()

logger = detailed_logger()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT = os.environ.get("TENANT")
SCOPES = os.environ.get("SCOPES")
FRONTEND = os.environ.get("FRONTEND")
REDIRECT_URI = "http://localhost:8000/token"
AUTHORITY_URL = "https://login.microsoftonline.com/common"  # f'https://login.microsoftonline.com/{TENANT}'
AUTH_ENDPOINT = "/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = "/oauth2/v2.0/token"
RESOURCE = "https://graph.microsoft.com/"
API_VERSION = "beta"
keys_url = "https://login.microsoftonline.com/common/discovery/keys"  # f'https://login.microsoftonline.com/{TENANT}/discovery/keys'
keys_raw = requests.get(keys_url).text
keys = json.loads(keys_raw)


pwd_context = CryptContext(schemes="bcrypt")

templates = Jinja2Templates(directory="static/templates")
oauth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearerCookie(
    tokenUrl="/api/token",
    scopes={
        "me": "Read information about the current user",
        "items": "Read items",
        "admin": "Full access",
    },
)
print("oauth2_scheme", oauth2_scheme.__dict__)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


@oauth_router.get("/auth/azure", include_in_schema=True)
async def azure_login():
    try:
        auth_state = str(uuid.uuid4())
        prompt_behavior = "select_account"  # prompt_behavior = 'login' select_account
        params = urllib.parse.urlencode(
            {
                "response_type": "code id_token",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "state": auth_state,
                "nonce": str(uuid.uuid4()),
                "prompt": prompt_behavior,
                "scope": SCOPES,
                "response_mode": "form_post",
            }
        )

        return RedirectResponse(AUTHORITY_URL + "/oauth2/v2.0/authorize?" + params)
    except Exception as error:
        return str(error)


@oauth_router.post("/token", include_in_schema=True)
async def azure_token(request: Request, db: Session = Depends(get_session)):
    try:
        body_form = await request.form()
        id_token = body_form.get("id_token")
        code = body_form.get("code")
        logger.info(f"code: {code}")
        id_token_decoded = json.loads(
            jws.verify(id_token, keys, algorithms=["RS256"], verify=False)
        )
        logger.info(f"id_token_decoded: {id_token_decoded}")
        username = id_token_decoded.get("preferred_username")
        email = id_token_decoded.get("email")
        issuer = id_token_decoded.get("iss")
        if not username and not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or password are incorrect!",
            )
        query = select(models.User).where(models.User.username == username)
        user = db.exec(query).first()
        if not user:
            user = models.User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": username,
                "issuer": issuer,
                "user_id": user.id,
                "hasProfile": True if user.profile else False,
                "scopes": user.scopes if user.scopes else "",
            },
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(
            user.id, user.username, minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 2
        )
        return RedirectResponse(
            f"{FRONTEND}/?token={access_token}&refresh_token={refresh_token}",
            status_code=303,
        )
    except Exception as e:
        logger.error(f"Error processing id_token: {e}")
        return RedirectResponse(f"{FRONTEND}/?token=false", status_code=303)


@oauth_router.post("/graph", include_in_schema=True)
async def ms_graph_get_token(code: str, graph_endpoint=None):
    """Get Access Token for Micorosft Graph and call the API"""
    auth_context = adal.AuthenticationContext(AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, REDIRECT_URI, RESOURCE, CLIENT_ID, CLIENT_SECRET
    )
    access_token = token_response["accessToken"]
    graph_endpoint = "https://graph.microsoft.com/beta/me/profile"
    headers = {"Authorization": "Bearer {}".format(access_token)}
    response = requests.get(graph_endpoint, headers=headers).json()
    return response


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    to_encode.update({"iat": datetime.datetime.utcnow()})
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire, "iss": "krassy"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int, username: str, minutes: str):
    refresh_token_data = {
        "sub": username,
        "user_id": user_id,
        "iat": datetime.datetime.utcnow(),
    }
    exp = datetime.datetime.utcnow() + timedelta(minutes=minutes)
    refresh_token_data.update({"exp": exp})
    refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def get_current_user(
    request: Request,
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expires = payload.get("exp")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", []).split(" ")
        token_data = models.TokenData(
            username=username, expires=expires, scopes=token_scopes
        )
    except jwt.ExpiredSignatureError as e:
        logger.error("jwt.ExpiredSignatureError")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.JWTError as error:
        logger.error("jwt.JWTError", error)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    except Exception as e:
        logger.error("Exception:", e)
        raise credentials_exception
    query = select(models.User).where(models.User.username == token_data.username)
    user = db.exec(query).first()
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

@oauth_router.post("/api/token/refresh", include_in_schema=True)
async def refresh_access_token(request: Request, db: Session = Depends(get_session)):
    try:
        data = await request.json()
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        try:
            data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError as error:
            raise HTTPException(status_code=401, detail=str(error))
        user_id = int(data.get("user_id"))
        user = db.exec(select(models.User).where(models.User.id == user_id)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "hasProfile": True if user.profile else False,
                "scopes": user.scopes if user.scopes else "",
            },
            expires_delta=access_token_expires,
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )


@oauth_router.post("/api/token", include_in_schema=True)
async def login_access_token(
    *,
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    query = select(models.User).where(models.User.username == form_data.username)
    data = request.__dict__
    remember_me = [v.get("rememberMe") for k, v in data.items() if k == "_form"][0]
    user = db.exec(query).first()
    if user and user.verify_password(form_data.password):
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 1)
        if remember_me == "true":
            access_token = create_access_token(
                data={
                    "sub": user.username,
                    "user_id": user.id,
                    "hasProfile": True if user.profile else False,
                    "scopes": user.scopes,
                },
                expires_delta=token_expires,
            )
            refresh_token = create_refresh_token(
                user.id, user.username, minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 2
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "refresh_token": refresh_token,
            }
        else:
            access_token = create_access_token(
                data={
                    "sub": user.username,
                    "user_id": user.id,
                    "hasProfile": True if user.profile else False,
                    "scopes": user.scopes,
                },
                expires_delta=token_expires,
            )
            refresh_token = create_refresh_token(
                user.id, user.username, minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 5
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "refresh_token": refresh_token,
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password are incorrect!",
        )


@oauth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, include_in_schema=False
)
async def signup(request: Request, db: Session = Depends(get_session)):
    form_data = await request.form()
    username = form_data.get("username")
    passwd = form_data.get("password")
    passwd2 = form_data.get("password2")
    if (username and passwd and passwd2) and passwd == passwd2:
        query = select(models.User).where(models.User.username == username)
        user = db.exec(query).first()
        if user:
            logger.error("User with that name already exists!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This Email is taken. Try another",
            )
        user = models.User(username=username)
        user.set_password(passwd)
        user.scopes = "me items"
        db.add(user)
        db.commit()
        logger.info(f"New user {user.username} has been created")
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Password did not match!"
    )


@oauth_router.get("/login", include_in_schema=False)
def login(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    return response


@oauth_router.post("/token_admin", include_in_schema=False)
def login_access_token_old(
    *,
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    query = select(models.User).where(models.User.username == form_data.username)
    user = db.exec(query).first()
    if user and user.verify_password(form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "scopes": user.scopes},
            expires_delta=access_token_expires,
        )
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)
        return response

    else:
        context = {"request": request, "message": "Username or password are incorrect!"}
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
