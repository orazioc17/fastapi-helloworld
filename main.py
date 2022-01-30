# Python
from typing import Optional
from enum import Enum  # Sirve para crear enumeraciones de string

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt, conint

# FastAPI
from fastapi import FastAPI, Body, Query, Path

# Inicializando la app
app = FastAPI()


# Model


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
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=35
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=35
    )


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        ...,
        gt=17,
        le=115
    )
    # De esta manera se declaran campos opcionales con valores por defecto
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: str = EmailStr(
        ...,
    )
    web_page: str = HttpUrl(
        ...,
    )
    identity: int = PositiveInt(...)


# Path operation de home - Get
@app.get("/")
def home():
    return {'hello': 'Hola mundo'}


# Request and Response Body


@app.post("/person/new")
def create_person(person: Person = Body(...)):  # Cada vez que se encuentre ese triple punto en fastapi, significa que
    # ese parametro es obligatorio
    return person


# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name. It's between 1 and 50 characters"
        ),
        age: int = Query(
            ...,
            gt=17,
            title="Person Age",
            description="This is the person age. This is a required parameter. It has to be greater than 17",
        )
):
    return {name: age}


# Validaciones: Path parameters

@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(
            ...,
            gt=0,
            title="Person Id",
            description="This is the person id. It has to be greater than 0"
        )
):
    return {person_id: "It exists!"}


# Validaciones: body parameters
@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id",
            gt=0
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
