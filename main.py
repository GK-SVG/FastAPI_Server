from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'gk'}}


@app.get('/about')
def about():
    return {'data':{'about':'i am engineer'}}