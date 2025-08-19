from fastapi import APIRouter,Depends,HTTPException,status
from models.model import Post,User
from models.schemas import *
from security import get_current_active_user
from database import connect 
from sqlalchemy.orm import Session

post_router=APIRouter(tags=['posts'],prefix='/posts')


@post_router.post('/new')
async def create_new_post(req:PostCreate,
    user:User=Depends(get_current_active_user),
    db:Session=Depends(connect)):
    post=Post(title=req.title,
            description=req.description,
            created_at=req.created_at,
            user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message":'post created successfully'}

@post_router.patch('/{id}/update')
async def update_post(id:int,req:PostUpdate,
                      user:User=Depends(get_current_active_user)
                      ,db:Session=Depends(connect)):
    post=db.query(Post).filter(Post.id==id).update(req.dict(),synchronize_session=False)
    
    db.commit()
    db.refresh(post)
    return {'message':'post updated successfully'}

@post_router.get('/all')
async def get_all_post(db:Session=Depends(connect),
                    user:User=Depends(get_current_active_user)):
    return db.query(Post).all()

@post_router.get('/{id}')
async def get_post(id:int,db:Session=Depends(connect),
    user:User=Depends(get_current_active_user)):
    post=db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(detail='post does not exist ',
        status_code=status.HTTP_404_NOT_FOUND)
    return post 

@post_router.post('/{id}/like')
async def like_a_post(id:int,
                    db:Session=Depends(connect),
                    user:User=Depends(get_current_active_user)):
    post=db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(detail='post not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    user.liked_posts.append(post)
    db.commit()
    return {'message':'you have like a post'}

@post_router.delete('/{id}/unlike')
async def unlike_a_post(id:int,db:Session=Depends(connect),
                        user:User=Depends(get_current_active_user)):
    post=db.query(Post).filter(Post.id==id).first()
    if not post:
        raise HTTPException(detail='post not found',
                            status_code=status.HTTP_400_BAD_REQUEST)
    post.liked_by.remove(user)
    db.commit()
