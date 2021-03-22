from fastapi import FastAPI,Depends,Response,HTTPException,status
from schema import Blog
import modals
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

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


@app.post('/blog',status_code = status.HTTP_201_CREATED)
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


@app.get('/blog/{id}',status_code=status.HTTP_200_OK)
def blog(id, db:Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    return blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db:Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    db.query(modals.Blog).filter(modals.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return f"blog with id {id} deleted" 


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:Blog,db:Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    update_item_encoded = jsonable_encoder(request)
    db.query(modals.Blog).filter(modals.Blog.id==id).update(update_item_encoded)
    db.commit()
    return f"blog with id {id} updated" 