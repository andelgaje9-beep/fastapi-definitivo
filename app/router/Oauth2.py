from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from .. import alchemy_models, database, schemasORM, utilshash 
from jose import jwt, JWTError
from app.config import settings


router = APIRouter(tags=["Authentication"])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="Tokenlogin")

# openssl rand --hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


@router.post("/Tokenlogin", response_model= schemasORM.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_session)):
    
    stmt = select(alchemy_models.User).where(alchemy_models.User.email == form_data.username)
    user = db.execute(stmt).scalar_one_or_none() 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not user found bro")
    
    if not utilshash.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Crear token JWT con el ID del usuario como "sub" (subject)
    access_token = create_access_token(data={"sub_id": str(user.id)})
    # Retornar el token y el tipo "bearer" para que el cliente lo use en Authorization header
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Aqui llega el token JWT que el cliente envio, credentials_exception: 
# es una excepción predefinida que se lanza si algo falla (ej. credenciales inválidas).
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub_id")
        if user_id is None:
            raise credentials_exception
        return schemasORM.TokenData(sub=user_id)
    except JWTError:
        raise credentials_exception
    
    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token_data = verify_access_token(token, credentials_exception)

    stmt = select(alchemy_models.User).where(alchemy_models.User.id == int(token_data.sub))
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    # Devuelve el usuario como esquema de salida
    return schemasORM.UserOut.model_validate(user)






    