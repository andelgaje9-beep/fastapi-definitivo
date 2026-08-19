from typing import Annotated
from fastapi import  HTTPException, Depends, status, APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .. import alchemy_models, schemasORM    
from ..database import get_session
from ..utilshash import hash_password
from .Oauth2 import get_current_user


router = APIRouter(prefix="/users",
                tags=["users"])

@router.post("/", status_code= status.HTTP_201_CREATED ,response_model= schemasORM.UserOut)
async def create_user(user:schemasORM.UserCreate, db: Annotated[ Session, Depends(get_session)]):
    hashed_password = hash_password(user.password)
    
    new_user = alchemy_models.User(email= user.email, password= hashed_password)
    
    db.add(new_user)
    
    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado"
        )

    return new_user

@router.get("/{id}", status_code= status.HTTP_200_OK,response_model= schemasORM.UserOut)
async def get_user(id: int, db: Annotated[ Session, Depends(get_session)],
                    current_user: Annotated[schemasORM.UserOut, Depends(get_current_user)]):
    stmt = select(alchemy_models.User).where(alchemy_models.User.id == id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user