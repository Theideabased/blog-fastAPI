from fastapi import APIRouter, Depends, status
from blog_fastAPI import database , schemas
from sqlalchemy.orm import Session
from blog_fastAPI.utils import user


router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(id:int, db: Session = Depends(database.get_db)):
    return user.get(id,db)