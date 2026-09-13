from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .token import get_current_user

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)
@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: models.User = Depends(get_current_user)  # noqa: B008
):
    post = db.execute(select(models.Post).where(models.Post.id == vote.post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(
                                    status_code = status.HTTP_404_NOT_FOUND,
                                    detail = "Post doesn't exist"
                                )
    vote_query = db.execute(select(models.Vote).where(models.Vote.post_id == vote.post_id, 
                    models.Vote.user_id == current_user.id))
    found_vote = vote_query.scalar_one_or_none()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"User with id: {current_user.id} already voted for post with id: {vote.post_id}"
            )
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                            status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Vote doesn't exist"
                        )
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote removed successfully"}