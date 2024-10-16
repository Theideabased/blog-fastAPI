from blog_fastAPI import database, schemas, models
from blog_fastAPI.hashing import Hash
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

def create(request: schemas.User, db: Session = Depends(database.get_db)):
    try:
        Hash.bcrypt(request.password)
    except:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_user = models.User(name=request.name, email=request.email, 
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()
    if not user:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with id {id} not found")
    return user