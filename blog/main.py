from fastapi import FastAPI,Depends
from schema import Blog
import modals
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

modals.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(request:Blog,db:Session = Depends(get_db)):
    new_blog = modals.Blog(title= request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog