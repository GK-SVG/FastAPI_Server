from fastapi import FastAPI,Depends
from schema import Blog
import modals
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
# print('fastApi Instance--',app)
# print('fastApi Database engine--',engine)

modals.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    # print("get_deb--",db)
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(request:Blog,db:Session = Depends(get_db)):
    # print("request--",request)
    # print("db--",db)
    new_blog = modals.Blog(title= request.title,body=request.body)
    # print("new_blog--",new_blog)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/allBlog')
def all_blog(db:Session = Depends(get_db)):
    blogs = db.query(modals.Blog).all()
    return blogs


@app.get('/blog/{id}')
def blog(id, db:Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id==id).first()
    return blog