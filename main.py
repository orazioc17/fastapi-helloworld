# Python
from typing import Optional
from enum import Enum  # Sirve para crear enumeraciones de string

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt, conint

# FastAPI
from fastapi import FastAPI, Body, Query, Path, status

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


# Path operation de home - Get ----- Aqui tambien se especifica el status code del response
@app.get(
    path="/",
    status_code=status.HTTP_200_OK
)
def home():
    return {'hello': 'Hola mundo'}


# Request and Response Body


@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
# Cada vez que se encuentre ese triple punto en fastapi, significa que ese parametro es obligatorio
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
)
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name. It's between 1 and 50 characters",
            example="Rocio"
        ),
        age: int = Query(
            ...,
            gt=17,
            title="Person Age",
            description="This is the person age. This is a required parameter. It has to be greater than 17",
            example=25
        )
):
    return {name: age}


# Validaciones: Path parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
)
def show_person(
        person_id: int = Path(
            ...,
            gt=0,
            title="Person Id",
            description="This is the person id. It has to be greater than 0",
            example=123
        )
):
    return {person_id: "It exists!"}


# Validaciones: body parameters
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED
)
def update_person(
        person_id: int = Path(
            ...,
            title="Person id",
            description="This is the person id",
            gt=0,
            example=123
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    # return results

    return {"person": person, "location": location}
