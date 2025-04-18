from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.product import _create_new_product, _delete_product, _get_product_by_id, _update_product
from api.actions.user import check_user_permissions
from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user, _delete_user, _get_user_by_id, _update_user
from api.models import DeleteProductResponse, ProductCreate, ShowProduct, UpdateProductRequest, UpdatedProductResponse, UserCreate, ShowUser, DeleteUserResponse, UpdateUserRequest, UpdatedUserResponse
from db.models import User
from db.session import get_db

user_router = APIRouter()
product_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
    ) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
        target_user=user_for_deletion,
        current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user

@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, 
        body: UpdateUserRequest, 
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse:
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    if user_id != current_user.user_id:
         if check_user_permissions(
             target_user=user_for_update, current_user=current_user
         ):
             raise HTTPException(status_code=403, detail="Forbidden.")
    updated_user_id = await _update_user(updated_user_params=updated_user_params, db=db, user_id=user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)

### Product handlers ###
@product_router.post("/", response_model=ShowProduct)
async def create_product(body: ProductCreate, db: AsyncSession = Depends(get_db)) -> ShowProduct:
    return await _create_new_product(body, db)

@product_router.patch("/", response_model=UpdatedProductResponse)
async def update_product_by_id(
        product_id: UUID, 
        body: UpdateProductRequest, 
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> UpdatedProductResponse:
    updated_product_params = body.model_dump(exclude_none=True)
    if updated_product_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for product update info should be provided")
    product_for_update = await _get_product_by_id(product_id, db)
    if product_for_update is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")

    if current_user.user_id != product_for_update.user_id:
        raise HTTPException(status_code=403, detail="Forbidden.")
         
    updated_product_id = await _update_product(updated_product_params=updated_product_params, session=db, product_id=product_id)
    return UpdatedProductResponse(updated_product_id=updated_product_id)

@product_router.get("/", response_model=ShowProduct)
async def get_product_by_id(product_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowProduct:
    product = await _get_product_by_id(product_id, db)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")
    return product

@product_router.delete("/", response_model=DeleteProductResponse)
async def delete_product(
    product_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
    ) -> DeleteProductResponse:

    product_for_deletion = await _get_product_by_id(product_id, db)
    if product_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} not found."
        )
    if current_user.user_id != product_for_deletion.user_id:
        raise HTTPException(status_code=403, detail="Forbidden.")
    
    deleted_product_id = await _delete_product(product_id, db)
    if deleted_product_id is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")
    
    return DeleteProductResponse(deleted_product_id=deleted_product_id)