import enum
from sqlalchemy import Column,INTEGER,String,ForeignKey,DateTime,Enum
# from database import Base
import datetime
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
class User(Base):
    __tablename__='User'
    
    id=Column(INTEGER,primary_key=True,autoincrement=True)
    fullname=Column(String(20))
    username=Column(String(20),unique=True)
    hashed_password=Column(String(100))
    

    
class typeoff(enum.Enum):
        INT="IN"
        OUT="out"    

class timestampuser(Base):
    __tablename__="timestampofuser"
    
    stampid=Column(INTEGER,primary_key=True,autoincrement=True)
    user_id=Column(INTEGER,ForeignKey('User.id'),nullable=True)
    time=Column(DateTime(timezone=True),default=datetime.datetime.utcnow)
    typeof=Column(Enum(typeoff))