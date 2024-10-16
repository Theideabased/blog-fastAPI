from fastapi import Depends, HTTPException, status
from blog_fastAPI import database
from sqlalchemy.orm import Session
from blog_fastAPI import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog ,db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==
                                 id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not in database")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"details": f"The blog with the {id} is deleted"}

def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'

def show(id, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Blog with the {id} is not available")

    return blog