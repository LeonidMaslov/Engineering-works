from typing import Union
from urllib.request import Request

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse


app = FastAPI()
#
# templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def read_root():
#     return {'Hello': 'World'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/1")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#
# @app.get("/", response_class=HTMLResponse)
# def read_item(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

#TODO Здесь нужна функция которая будет брать из БД какие то данные (похуй какие) и отдавать в return эти данные


