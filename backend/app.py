from fastapi import Response, Request, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, Session, select
from db import engine
from routers.categories import category_router
from routers.items import items_router
from routers.reviews import reviews_router
from routers.profile import profile_router
from auth.oauth import oauth_router, get_current_user, SECRET_KEY, ALGORITHM
import models
from pathlib import Path
import os
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from jose import jwt
from models import Category, Categories, User, Item, Review, UserProfile
from my_logger import detailed_logger
from datetime import datetime, timedelta
from starlette_admin.contrib.sqla import Admin, ModelView
from dotenv import load_dotenv

load_dotenv()
# from prometheus_fastapi_instrumentator import Instrumentator

PROJECT_ROOT = Path(__file__).parent.parent # /
BASE_DIR = Path(__file__).resolve().parent # / src
PROTECTED = [Depends(get_current_user)]

templates = Jinja2Templates(directory=Path(BASE_DIR, 'static/templates'))

app = FastAPI() # docs_url=None
app.include_router(category_router)
app.include_router(items_router)
app.include_router(reviews_router)
app.include_router(oauth_router)
app.include_router(profile_router)

origins = [
    "http://localhost:8081",
    "http://localhost:3000"
]

admin = Admin(
    engine,
    title="Auth",
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Item))
admin.add_view(ModelView(Review))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(UserProfile))

admin.mount_to(app)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = detailed_logger()

@app.middleware("http")
async def add_content_security_policy_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
    return response

@app.middleware("http")
async def admin_panel_middleware(request: Request, call_next):
    response = JSONResponse(
                    status_code=401,
                    content={"message": "Token has expired!"},
                )
    if request.url.path.startswith("/admin"):
        if request.cookies.get("access_token") is not None:
            token: str = request.cookies.get("access_token")
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                expires = payload.get("exp")
                scopes = payload.get("scopes")
                if username is None:
                    response.delete_cookie("access_token")
                    return response
                token_data = models.TokenData(username=username, expires=expires)
            except jwt.ExpiredSignatureError:
                response.delete_cookie("access_token")
                return response
            except jwt.JWTError:
                response.delete_cookie("access_token")
                return response
            except Exception:
                response.delete_cookie("access_token")
                return response
            with Session(engine) as session:
                statement = select(models.User).where(models.User.username == token_data.username)
                user = session.exec(statement).first()
                if user and 'admin' in scopes:
                    response = await call_next(request)
                    return response
                else:
                   return Response('Unauthorized!')
        else:
            return RedirectResponse(url='/login', status_code=303)
    else:
        response = await call_next(request)
        return response

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    create_categories(engine)
    app.mount("/static", StaticFiles(directory=Path(BASE_DIR, 'static'),html=True),name="static")
    # instrumentator.expose(app)

@app.get("/static/img/{image_path:path}", include_in_schema=False)
async def get_image(image_path: str):
    full_image_path = os.path.join(BASE_DIR, f'static/img/{image_path}')
    with open(full_image_path, "rb") as file:
        image_content = file.read()
    response = Response(content=image_content)
    response.headers["Cache-Control"] = "max-age=604800"
    response.headers["Expires"] = (datetime.utcnow() + timedelta(hours=168)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response

def create_categories(engine):
    with Session(engine) as session:
        cat = session.query(Category).all()
        if not cat:
            for c in Categories:
                category = Category(name=c)
                session.add(category)
            session.commit()
            session.refresh(category)




