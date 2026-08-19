from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


"""CLASES PARA USERS.PY"""
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
        
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 
    
    model_config = ConfigDict(from_attributes=True)


"""CLASES PARA POSTS.PY"""
class PostBase(BaseModel):
    title: str
    content: str 
    published: bool= True
    
    
class PostCreate(PostBase):
    pass 

class PostOut(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut

    
    # Permite que el modelo lea atributos directamente de objetos ORM (ej. SQLAlchemy),
    # no solo diccionarios, reemplazando el antiguo `orm_mode=True` de Pydantic v1
    # solo se usa en las salidas para serializar ORM a json valido
    model_config = ConfigDict(from_attributes=True)


"""CLASE PARA AUTHJWTBEARER.PY"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

"""CLASE PARA Oauth2.PY"""
# Modelo para tokens de acceso (respuesta al login)
class Token(BaseModel):
    access_token : str      # Token JWT generado
    token_type : str        # Tipo de token (ej. "bearer")
    
    
# Modelo para datos dentro del token (claims)
class TokenData(BaseModel):
    sub: Optional[str] = None   # Identificador del usuario (ej. email o ID)
    
"""CLASE PARA VOTES.PY"""
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1, ge=0)]
    # Dirección del voto: 1 = agregar voto, 0 = eliminar voto
    # Validado para que solo acepte valores entre 0 y 1