# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path

# Inicializando la app
app = FastAPI()


# Model

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    # De esta manera se declaran campos opcionales con valores por defecto
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


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
