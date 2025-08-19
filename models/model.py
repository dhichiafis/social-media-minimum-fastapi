from sqlalchemy import Table,Column,Integer,ForeignKey,String,Index,DateTime,Text,func,DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime

from database import *

class Like(Base):
    __tablename__='likes'
    user_id=Column('user_id',ForeignKey('users.id'),primary_key=True)
    post_id=Column('post_id',ForeignKey('posts.id'),primary_key=True)
    
follows=Table(
    'follows',
    Base.metadata,
    Column('follower_id',ForeignKey('users.id'),primary_key=True),
    Column('following_id',ForeignKey('users.id'),primary_key=True)
)

class User(Base):
    __tablename__='users'
    id=Column('id',Integer,primary_key=True)
    username=Column('username',String,unique=True,index=True)
    password=Column('password',String)
    created_at=Column('created_at',DateTime(),default=datetime.now(),nullable=False)
    comments=relationship('Comment',back_populates='user')
    posts=relationship('Post',back_populates='user')
    liked_posts=relationship('Post',secondary='likes',back_populates='liked_by')
    
    followers=relationship('User',
        secondary='follows',
        primaryjoin=id==follows.c.following_id,
        secondaryjoin=id==follows.c.follower_id
        ,back_populates='following')
    
    following=relationship('User',secondary='follows',
        primaryjoin=id==follows.c.follower_id,
        secondaryjoin=id==follows.c.following_id,
        back_populates='followers'
        )
    
class Post(Base):
    __tablename__='posts'
    id=Column('id',Integer,primary_key=True)
    user_id=Column('user_id',Integer,ForeignKey('users.id'))
    title=Column('title',String,index=True)
    description=Column('description',Text)
    created_at=Column('created_at',DateTime,default=datetime.now())
    user=relationship('User',back_populates='posts')
    comments=relationship('Comment',back_populates='post')
    liked_by=relationship('User',secondary='likes',back_populates='liked_posts')
    
    
class Comment(Base):
    __tablename__='comments'
    id=Column('id',Integer,primary_key=True)
    user_id=Column('user_id',Integer,ForeignKey('users.id'))
    post_id=Column('post_id',Integer,ForeignKey('posts.id'))
    description=Column('description',Text)
    created_at=Column('created_at',DateTime(),default=datetime.now())
    user=relationship('User',back_populates='comments')
    post=relationship('Post',back_populates='comments')