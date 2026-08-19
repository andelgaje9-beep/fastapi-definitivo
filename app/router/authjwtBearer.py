from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import alchemy_models, database, schemasORM, utilshash 


router = APIRouter(tags=["Authentication sin Token"])


@router.post("/login")
async def login(user_credentials: schemasORM.UserLogin, db: Session = Depends(database.get_session)):
    
    stmt = select(alchemy_models.User).where(alchemy_models.User.email == user_credentials.email)
    user = db.execute(stmt).scalar_one_or_none() 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not user found bro")
    
    if not utilshash.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"token": "example token"}
