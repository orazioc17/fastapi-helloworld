# Python
from typing import Optional

from enum import Enum  # Sirve para crear enumeraciones de string

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=35,
        example="San Cristobal"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=35,
        example="Tachira"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=35,
        example="Venezuela"
    )


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
    )
    age: int = Field(
        ...,
        gt=17,
        le=115,
        example=21
    )
    # De esta manera se declaran campos opcionales con valores por defecto
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)
    email: str = EmailStr(
        ...,
    )
    web_page: str = HttpUrl
    identity: int = PositiveInt

    # class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Facundo",
    #            "last_name": "Garcia",
    #            "age": 21,
    #            "hair_color": "blonde",
    #            "is_married": False
    #        }
    #    }


class Person(PersonBase):

    password: str = Field(..., min_length=8)


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfuly!")
