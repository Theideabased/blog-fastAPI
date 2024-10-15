from fastapi import APIRouter, Depends
from blog-fastapiimport schemas, database, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs