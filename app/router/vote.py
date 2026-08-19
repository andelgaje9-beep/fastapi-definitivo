from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemasORM, alchemy_models
from . import Oauth2
from sqlalchemy.orm import Session
from ..database import get_session
from sqlalchemy import select

router = APIRouter(prefix="/vote",
                tags= ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemasORM.Vote, db: Session = Depends(get_session), 
            current_user: schemasORM.UserOut = Depends(Oauth2.get_current_user)):
    
    post = db.query(alchemy_models.Post).where(alchemy_models.Post.id == vote.post_id). first()
        
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    stmt = select(alchemy_models.Vote).where(
        alchemy_models.Vote.post_id == vote.post_id, alchemy_models.Vote.user_id == current_user.id)
    found_vote = db.execute(stmt).scalar_one_or_none()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )
        new_vote = alchemy_models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="vote does not exist"
            )
        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}