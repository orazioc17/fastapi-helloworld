# Python
from typing import Optional

# FastAPI
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie, UploadFile, File, HTTPException

# Pydantic
from pydantic import EmailStr

# Models
from models import Person, PersonOut, Location, LoginOut

# Inicializando la app
app = FastAPI()


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
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)
# Cada vez que se encuentre ese triple punto en fastapi, significa que ese parametro es obligatorio
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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


persons = [1, 2, 3, 4, 5]


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists"
        )
    return {person_id: "It exists!"}


# Validaciones: body parameters
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
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


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
# Aqui se recibe un formulario desde el frontend --- Recordar que ... es para indicar que es obligatorio
def login(username: str = Form(...), password: str = Form(...)):
    # return LoginOut esto daba error porque se debia retornar un json y estabamos retornando la clase
    return LoginOut(username=username)


# Cookies and Headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    # ads controla las cookies que nos envia el servidor que tenemos trabajando con la api
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Working with files
@app.post(
    path="/post-image"
)
def post_image(
        image: UploadFile = File(...)
):
    # FastAPI se encargara de transformar automaticamente este diccionario a un json
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
