from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends

from api.models import ProductCreate, ShowProduct
from db.dals import ProductDAL
from db.models import Product, User
from db.session import get_db
from hashing import Hasher

product_router = APIRouter()


async def _create_new_product(body: ProductCreate, session) -> ShowProduct:
    async with session.begin():
        product_dal = ProductDAL(session)
        product = await product_dal.create_product(
            user_id=body.user_id,
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
            user_id=product.user_id,
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

async def _get_product_by_id(product_id, session) -> Union[Product, None]:
    async with session.begin():
        product_dal = ProductDAL(session)
        product = await product_dal.get_product_by_id(
            product_id=product_id,
        )
        if product is not None:
            return product

async def _update_product(updated_product_params: dict, product_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        product_dal = ProductDAL(session)
        updated_product_id = await product_dal.update_product(
            product_id=product_id,
            **updated_product_params
        )
        return updated_product_id

async def _delete_product(product_id, session) -> Union[UUID, None]:
    async with session.begin():
        product_dal = ProductDAL(session)
        deleted_product_id = await product_dal.delete_product(
            product_id=product_id,
        )
        return deleted_product_id