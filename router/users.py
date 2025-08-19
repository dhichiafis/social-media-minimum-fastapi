from fastapi import APIRouter,Depends,status,Query
from security import *
from database import *
from sqlalchemy.orm import Session
from models.model import *
from models.schemas import *

users_router=APIRouter(tags=['users'],prefix='/users')


@users_router.post('/new')
async def create_new_user(req:UserCreate,db:Session=Depends(connect)):
    user_db=db.query(User).filter(User.username==req.username).first()
    if user_db:
        raise HTTPException(detail="user with specified username already exist",status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    password=get_password_hash(req.password)
    user=User(username=req.username,password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":'user created successfully'}


@users_router.get("/all",response_model=list[UserBase])
async def get_all_users(db:Session=Depends(connect)):
    return db.query(User).all()


@users_router.get('/',response_model=UserBase)
async def get_user(id:int,db:Session=Depends(connect)):
    user= db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(detail='user not found',status_code=status.HTTP_404_NOT_FOUND)
    return user 

@users_router.get('/',response_model=UserBase)
async def get_user_by_username(username:str=Query(...,
        description="the username"),db:Session=Depends(connect)):
    user=db.query(User).filter(User.username==username).first()
    return user

@users_router.post("/token")
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(connect)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@users_router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    current_user: User=Depends(get_current_active_user),
):
    return current_user


@users_router.post('/follow')
async def follow_users(id:int,db:Session=Depends(connect),
                    user:User=Depends(get_current_active_user)):
    follow=db.query(User).filter(User.id==id).first()
    user.following.append(follow)
    db.commit()
    db.refresh(user)
    return {'message':f'you have succefully followed {follow.username}'}
    