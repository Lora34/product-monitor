from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends

from api.models import ProductCreate, ShowProduct
from db.dals import ProductDAL
from db.models import User
from db.session import get_db
from hashing import Hasher

product_router = APIRouter()


async def _create_new_product(body: ProductCreate, session) -> ShowProduct:
    async with session.begin():
        product_dal = ProductDAL(session)
        product = await product_dal.create_product(
            name=body.name,
            description=body.description,
            link_to_product=body.link_to_product,
            price=body.price,
            logo=body.logo,
            about=body.about,
            problem=body.problem,
            decision=body.decision,
            advantages=body.advantages,
            additional=body.additional,
            link=body.link,
            #born_date=body.born_date,
            #post_date=body.post_date,
            pictures=body.pictures
        )
        return ShowProduct(
            product_id=product.product_id,
            name=product.name,
            description=product.description,
            link_to_product=product.link_to_product,
            price=product.price,
            logo=product.logo,
            about=product.about,
            problem=product.problem,
            decision=product.decision,
            advantages=product.advantages,
            additional=product.additional,
            link=product.link,
            #born_date=product.born_date,
            #post_date=product.post_date,
            pictures=product.pictures
        )