from fastapi import APIRouter
from .. import schemas
router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: schemas.Login):
    return 'login'