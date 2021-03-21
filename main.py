from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'gk'}}


@app.get('/about')
def about():
    return {'data':{'about':'i am engineer'}}


@app.get('/blog/{id}')
def blog(id:int):
    return {'data':{'blog':id}}


class Blog(BaseModel):
    title:str
    body:str
    publised_at:Optional[bool]


@app.post('/blog/comment')
def blog(request:Blog):
    return {'data':{'blog':Blog.title}}