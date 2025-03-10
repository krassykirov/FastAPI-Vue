import datetime
import decimal
from pydantic import BaseModel, EmailStr
from typing import Optional, Union, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR, Session
from sqlalchemy import JSON, func, Boolean
from sqlalchemy_utils import ChoiceType
import enum
from typing import Optional, List
import datetime
import uuid
from auth.oauth import pwd_context

class BaseSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    expires: Optional[datetime.datetime]
    scopes: Optional[list[str]] = []
class RefreshToken(BaseModel):
    username: Union[str, None] = None
    expires: Optional[datetime.datetime]

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    username: Optional[EmailStr]= Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""
    items: List['Item'] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="owner")
    reviews: List['Review'] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="user")
    profile: Optional['UserProfile'] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates='user')
    scopes: Optional[str] = Field(sa_column=Column("scopes", VARCHAR, unique=False, default=""))
    def set_password(self,password):
        self.password_hash = pwd_context.hash(password)
    def verify_password(self,password):
        return pwd_context.verify(password,self.password_hash)

class UserRead(SQLModel):
    id: int
    username: Optional[str]

class UserProfile(BaseSQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    profile_id: int = Field(default=None, foreign_key="user.id", unique=True)
    user:    Optional['User']  = Relationship(back_populates='profile')
    email:   Optional[EmailStr]
    primary_email: Optional[str]
    number:  Optional[str]
    address: Optional[str]
    avatar:  Optional[str]

class Item(SQLModel, table=True):
    id:             Optional[int] = Field(default=None, primary_key=True)
    name:           Optional[str] = Field(default=None, unique=True)
    product_code:   Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, nullable=False)
    date:           Optional[datetime.datetime] = Field(default=datetime.datetime.now().replace(microsecond=0), nullable=False)
    price:          Optional[decimal.Decimal] = Field(default=0, max_digits=6, decimal_places=2)
    image:          Optional[str] = Field(default="no-image.png")
    images:         Optional[Dict[Any,Any]] = Field(default={}, sa_column=Column(JSON))
    reviews:        Optional[List['Review']] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates='item')
    category_id:    Optional[int] = Field(default=None, foreign_key="category.id")
    category:       Optional['Category'] = Relationship(back_populates='items')
    owner:          Optional[User] = Relationship(back_populates="items")
    username:       Optional[str] = Field(default=None, foreign_key="user.username")
    description:    Optional[str]
    in_cart:        Optional[Dict[Any,Any]] = Field(default={}, sa_column=Column(JSON))
    liked:          Optional[Dict[Any,Any]] = Field(default={}, sa_column=Column(JSON))
    discount:       Optional[decimal.Decimal]
    discount_price: Optional[decimal.Decimal]
    quantity:       Optional[int] = Field(default=1)
    brand:          Optional[str] = Field(default=None)
    rating:         Optional[int] = Field(default=0)
    review_number:  Optional[int] = Field(default=0)
    rating_float:   Optional[decimal.Decimal] = Field(default=decimal.Decimal(0))


    def update_ratings(self, db: Session):
        result = db.query(func.avg(Review.rating).label("avg_rating"),
                          func.count(Review.id).label("review_count")).filter(Review.item_id == self.id).one()
        self.rating = round(result.avg_rating or 0)
        self.review_number = result.review_count or 0
        self.rating_float = decimal.Decimal(result.avg_rating or 0)
        db.commit()

    def update_discount(self):
        if self.discount:
            self.discount_price = round((self.price - self.price  * self.discount), 2)
        else:
            self.discount_price = round((self.price), 2)

    class Config:
        arbitrary_types_allowed = True

class Categories(str, enum.Enum):
    Laptops = "Laptops"
    Smartphones = "Smartphones"
    Tablets = "Tablets"
    Smartwatches = "Smartwatches"
    TV = "TV"

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[Categories] = Field(sa_column=Column(ChoiceType(Categories), unique=True))
    items: Optional[List['Item']] = Relationship(back_populates='category')
    class Config:
        schema_extra = {
            "example": {
                "name": "Category-1",
              }
            }

class Review(SQLModel, table=True):
    id:           Optional[int]    = Field(default=None, primary_key=True)
    text:         Optional[str]    = Field(default=None)
    item:         Optional['Item'] = Relationship(back_populates='reviews')
    item_id:      Optional[int]    = Field(default=None, foreign_key="item.id")
    rating:       Optional[int]    = Field(default=0)
    created_by:   Optional[str]    = Field(default=None, foreign_key="user.username")
    user:         Optional['User'] = Relationship(back_populates='reviews')
    user_avatar:  Optional[str]    = Field(default=None)
    date:         Optional[datetime.datetime] = Field(default=datetime.datetime.now().replace(microsecond=0), nullable=False)
