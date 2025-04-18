from datetime import date
from typing import Union
from uuid import UUID
from enum import Enum
from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Product, User

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################

class PortalRole(str, Enum):
     ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
     ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
     ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"

class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, 
        name: str, 
        surname: str, 
        email: str, 
        hashed_password: str, 
        roles: list[PortalRole],
        username: str,
        current_company: str,
        your_role: str,
        headline: str,
        about: str,
        links: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
            username=username,
            current_company=current_company,
            your_role=your_role,
            headline=headline,
            about=about,
            links=links

        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
    
    async def get_user_by_email(self, email: str) -> Union[User, None]:
         query = select(User).where(User.email == email)
         res = await self.db_session.execute(query)
         user_row = res.fetchone()
         if user_row is not None:
             return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = update(User). \
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(kwargs). \
            returning(User.user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

class ProductDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(
        self, 
        user_id: str,
        name: str, 
        description: str, 
        link_to_product: str, 
        price: str, 
        logo: str,
        about: str,
        problem: str,
        decision: str,
        advantages: str,
        additional: str,
        link: str,
        #born_date: date,
        #post_date: date,
        pictures: str
    ) -> Product:
        new_product = Product(
            user_id=user_id,
            name=name,
            description=description, 
            link_to_product=link_to_product,
            price= price,
            logo=logo,
            about=about,
            problem=problem,
            decision=decision,
            advantages=advantages,
            additional=additional,
            link=link,
            #born_date=born_date,
            #post_date=post_date,
            pictures=pictures
        )
        
        self.db_session.add(new_product)
        await self.db_session.flush()
        return new_product
    
    async def get_product_by_id(self, product_id: UUID) -> Union[Product, None]:
        query = select(Product).where(Product.product_id == product_id)
        res = await self.db_session.execute(query)
        product_row = res.fetchone()
        if product_row is not None:
            return product_row[0]
    
    async def update_product(self, product_id: UUID, **kwargs) -> Union[UUID, None]:
        query = update(Product). \
            where(Product.product_id == product_id). \
            values(kwargs). \
            returning(Product.product_id)
        res = await self.db_session.execute(query)
        update_product_id_row = res.fetchone()
        if update_product_id_row is not None:
            return update_product_id_row[0]

    async def delete_product(self, product_id: UUID) -> Union[UUID, None]:
        query = update(Product).\
            where(and_(Product.product_id == product_id)).\
            values(is_active=False).\
            returning(Product.product_id)
        res = await self.db_session.execute(query)
        deleted_product_id_row = res.fetchone()
        if deleted_product_id_row is not None:
            return deleted_product_id_row[0]
    