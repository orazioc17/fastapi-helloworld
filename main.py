# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query

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
        name: Optional[str] = Query(None, min_length=1, max_length=50),
        age: str = Query(...)
):
    return {name: age}
