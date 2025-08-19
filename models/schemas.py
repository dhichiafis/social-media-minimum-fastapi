from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class CommentCreate(BaseModel):
    description:str 
    created_at:datetime 
    
class CommentBase(CommentCreate):
    id:int 
    class Config:
        orm_mode=True 

class PostCreate(BaseModel):
    title:str 
    description:str 
    created_at:datetime 
    
class PostUpdate(PostCreate):
    pass 
class PostBase(PostCreate):
    id:int 
    user_id:int 
    comments:list[CommentBase]
    
    class Config:
        orm_mode=True


class UserRead(BaseModel):
    username:str 
    created_at:datetime
    
class UserCreate(UserRead):
    password:str 
    
class UserBase(UserRead):
    id:int 
    posts:list[PostBase]
    class Config:
        orm_mode=True 