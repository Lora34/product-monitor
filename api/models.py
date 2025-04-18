from datetime import date
import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, validator, constr

#########################
# BLOCK WITH API MODELS #
#########################

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    username: str
    current_company: str
    your_role: str
    headline: str
    about: str
    links: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    username: str
    current_company: str
    your_role: str
    headline: str
    about: str
    links: str

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    current_company: Optional[str]
    your_role: Optional[str]
    headline: Optional[str]
    about: Optional[str]
    links: Optional[str]

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value

class Token(BaseModel):
     access_token: str
     token_type: str

### Product ###
class ShowProduct(TunedModel):
    product_id: uuid.UUID
    user_id: str
    name: str 
    description: str 
    link_to_product: str 
    price: str 
    logo: str
    about: str
    problem: str
    decision: str
    advantages: str
    additional: str
    link: str
    #born_date: date
    #post_date: date
    pictures: str

class ProductCreate(BaseModel):
    user_id: str
    name: str 
    description: str 
    link_to_product: str 
    price: str 
    logo: str
    about: str
    problem: str
    decision: str
    advantages: str
    additional: str
    link: str
    #born_date: date
    #post_date: date
    pictures: str

class UpdatedProductResponse(BaseModel):
    updated_product_id: uuid.UUID

class UpdateProductRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    link_to_product: Optional[EmailStr]
    logo: Optional[str]
    about: Optional[str]
    problem: Optional[str]
    decision: Optional[str]
    advantages: Optional[str]
    additional: Optional[str]
    link: Optional[str]

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value