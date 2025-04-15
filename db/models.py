import datetime
import uuid

from enum import Enum
from sqlalchemy import Date, ForeignKey

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAEnum

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()

class ProductStatus(str, Enum):  # наследуем str, чтобы хорошо работало с Pydantic/FastAPI
    status1 = "В поиске  ментора",
    status2 = "В поиске сооснователя",
    status3 = "Беру на стажировку",
    status4 = "В поиске инвестиции",
    status5 = "В поиске людей в команду",
    status6 = "В поиске отзывовб оценки",
    status7 = "В поиске партнерства и коллабы"

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    current_company: Mapped[str] = mapped_column(String, nullable=True)
    your_role: Mapped[str] = mapped_column(String, nullable=True)
    headline: Mapped[str] = mapped_column(String, nullable=True)
    about: Mapped[str] = mapped_column(String, nullable=True)
    links: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    link_to_product: Mapped[str] = mapped_column(String, nullable=True)
    categories: Mapped[list["Category"]] = relationship(back_populates="product_id") #Категории - [{ id, name, path }]
    price: Mapped[str] = mapped_column(String, nullable=True)
    logo: Mapped[str] = mapped_column(String, nullable=True)
    about: Mapped[str] = mapped_column(String, nullable=True)
    problem: Mapped[str] = mapped_column(String, nullable=True)
    decision: Mapped[str] = mapped_column(String, nullable=True)
    advantages: Mapped[str] = mapped_column(String, nullable=True)
    additional: Mapped[str] = mapped_column(String, nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=True)
    status_of_project: Mapped[ProductStatus] = mapped_column(SQLAEnum(ProductStatus, name="product_status_enum"), nullable=False)
    #audience: Mapped[int] = mapped_column(Integer, nullable=True)
    born_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    post_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    pictures = Column(ARRAY(String), nullable=True) #Галерея - массив изображений продукта


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[int] = mapped_column(Integer, nullable=False)   
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    #author: Mapped[User] = relationship(back_populates="posts")