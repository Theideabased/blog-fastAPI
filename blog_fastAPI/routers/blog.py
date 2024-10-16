from fastapi import APIRouter, Depends, status
from blog_fastAPI import schemas, database
from sqlalchemy.orm import Session
from typing import List
from blog_fastAPI.utils import blog


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db:Session = Depends(database.get_db)):
    return blog.delete(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request,db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db:Session = Depends(database.get_db)):
    return blog.show(id, db)
