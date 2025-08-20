from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

#Base=declarative_base()

class Base(DeclarativeBase):
    pass 

DB_URL="sqlite:///third.db"

engine=create_engine(DB_URL)


SessionFactory=sessionmaker(bind=engine,autoflush=False,autocommit=False)


def connect():
    db=SessionFactory()
    try:
        yield db 
    finally:
        db.close()