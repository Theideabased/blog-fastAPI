from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
import schemas
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from hashing import Hash
from routers import blog

app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(blog.router)
# models.Base.metadata.drop_all(engine, tables=[models.User.__table__])
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return {"details": f"The blog with the {id} is deleted"}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'


# @app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog,tags=['blogs'])
def show(id,response: Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog with the {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'details': f"Blog with the {id} is not available"}
    return blog


@app.post('/user', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED,tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, 
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser, status_code=status.HTTP_200_OK, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()
    if not user:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with id {id} not found")
    return user