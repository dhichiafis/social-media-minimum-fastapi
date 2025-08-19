from fastapi import APIRouter,Depends

comments_router=APIRouter(prefix='/comments',tags=['comments'])

from fastapi import APIRouter,Depends,HTTPException,status
from models.model import Post,User,Comment 
from models.schemas import *
from security import get_current_active_user
from database import connect 
from sqlalchemy.orm import Session

comments_router=APIRouter(tags=['comments'],prefix='/comments')


@comments_router.post('/{id}/new')
async def create_new_comment(id:int,req:CommentCreate,
    user:User=Depends(get_current_active_user),
    db:Session=Depends(connect)):
    post=db.query(Post).filter(Post.id==id).first()
    comment=Comment(
            description=req.description,
            created_at=req.created_at,
            post_id=post.id,
            user_id=user.id)
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return {"message":'post created successfully'}

@comments_router.patch('/{id}/update')
async def update_comment(id:int,req:CommentCreate,
                      user:User=Depends(get_current_active_user)
                      ,db:Session=Depends(connect)):
    comment=db.query(Comment).filter(Comment.id==id).update(req.dict(),synchronize_session=False)
    
    db.commit()
    db.refresh(comment)
    return {'message':'post updated successfully'}

@comments_router.get('/all')
async def get_all_comments(db:Session=Depends(connect),
                    user:User=Depends(get_current_active_user)):
    return db.query(Comment).all()

@comments_router.get('/{id}')
async def get_post(id:int,db:Session=Depends(connect),
    user:User=Depends(get_current_active_user)):
    post=db.query(Comment).filter(Comment.id==id).first()
    if not post:
        raise HTTPException(detail='comment does not exist ',
        status_code=status.HTTP_404_NOT_FOUND)
    return post 


