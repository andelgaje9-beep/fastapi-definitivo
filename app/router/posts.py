from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import func, select
from typing import Annotated, List, Optional
from .. import alchemy_models, schemasORM
from ..database import get_session
from .Oauth2 import get_current_user

router = APIRouter(prefix="/posts",
    tags=["posts"])


# siempre debe ir en plurar el path por convencion
@router.get("/", response_model= List[schemasORM.PostOut])
async def get_all_posts(db: Annotated[ Session, Depends(get_session)]):
    try: 
        # select(models.Post) indica que queremos todos los registros de la tabla Post
        stmt = select(alchemy_models.Post)
        # Ejecutamos la sentencia en la sesión
        # .scalars() extrae directamente los objetos ORM (instancias de Post)
        # .all() devuelve todos los resultados en una lista
        all_posts = db.execute(stmt).scalars().all()
        return all_posts
    
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")


@router.get("/{id}", response_model= schemasORM.PostOut)
async def get_post_id(id: int, db: Annotated[ Session, Depends(get_session)],
                    current_user: Annotated[schemasORM.UserOut, Depends(get_current_user)]):
    stmt= select(alchemy_models.Post).where(alchemy_models.Post.id == id)
    print(stmt)
    
    #forma de imprimir la sentencia SQL para ver si esta bien
    # print(stmt.compile(compile_kwargs={"literal_binds": True}))
    post = db.execute(stmt).scalar_one_or_none() #este escalar lanza none(no lanza excepcion)
    print(post)
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemasORM.PostOut)
async def create_post(post: schemasORM.PostCreate, db: Annotated[ Session, Depends(get_session)], 
                    current_user: schemasORM.UserOut = Depends(get_current_user)):
    print(current_user.email)
    
    try:
        new_post = alchemy_models.Post(owner_id = current_user.id,**post.model_dump()) #Evita escribir campo por campo:
        # new_post = models.Post(title=post.title, content=post.content, published=post.published)
        
        print(new_post)

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return new_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Violación de integridad en la base de datos")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Annotated[ Session, Depends(get_session)],
                    current_user: Annotated[schemasORM.UserOut, Depends(get_current_user)]):
    try:
        stmt= select(alchemy_models.Post).where(alchemy_models.Post.id == id)
        delete_post = db.execute(stmt).scalar_one_or_none()
        
        if delete_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if delete_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "not AUTHORIZED")
        
        db.delete(delete_post)
        db.commit()
        return delete_post
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error") 



@router.put("/{id}", response_model= schemasORM.PostOut)
async def update_post(id: int, post: schemasORM.PostCreate, db: Annotated[ Session, Depends(get_session)],
                    current_user: Annotated[schemasORM.UserOut, Depends(get_current_user)]):
    try:
        stmt = select(alchemy_models.Post).where(alchemy_models.Post.id == id)
        existing_post = db.execute(stmt).scalar_one_or_none()
        
        if existing_post is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Post con {id} not found") 
        
        if existing_post.owner_id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "not AUTHORIZED")
        
        for key, value in post.model_dump().items():
            setattr(existing_post, key, value)
            
        db.commit()
        db.refresh(existing_post)
        return existing_post
    
    except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")
                
    
    
@router.get("/", response_model=List[schemasORM.PostBase])
async def get_posts(db: Session = Depends(get_session),current_user: schemasORM.UserOut = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    try:
        # Construir consulta base
        stmt = select(alchemy_models.Post)

        # Filtro de búsqueda
        if search:
            stmt = stmt.where(
                alchemy_models.Post.title.ilike(f"%{search}%") |
                alchemy_models.Post.content.ilike(f"%{search}%")
            )

        # Paginación
        stmt = stmt.offset(skip).limit(limit)

        # Mostrar el SQL generado (para depuración)
        # print(
        #     stmt.compile(
        #         dialect=postgresql.dialect(),
        #         compile_kwargs={"literal_binds": True}
        #     )
        # )

        # Ejecutar consulta y obtener lista de posts
        posts = db.execute(stmt).scalars().all()
        
        #ejecutar consulta con joins
        statement = select(alchemy_models.Post, func.count(alchemy_models.Vote.post_id).label('votes')).join(
            alchemy_models.Vote, alchemy_models.Vote.post_id == alchemy_models.Post.id, isouter=True).group_by(alchemy_models.Post.id)
        result = db.execute(statement).scalars().all()
        
        print(
            statement.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True}
            )
        )

        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            
            






