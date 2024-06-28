from sqlalchemy import text
import datetime
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import extract
from sqlalchemy.orm import Session
from database import local_session, engine
from schemas import user_register, user_login
from models import User, timestampuser, typeoff
from passlib.context import CryptContext
from starlette import status
import models
from jose import jwt, JWTError
import time
from AuthService import AuthService
from PunchService import PunchService
from UserService import UserService

app = FastAPI()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


@app.post('/user/create', tags=["user"])
def create_user(user: user_register, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)


@app.post('/user/login', tags=['user'])
def login(user_body: user_login, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_body.username, user_body.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    token = auth_service.create_jwt(user_body.username)
    return {"token": token}


@app.get('/userbytoken')
def userbytoken(token: str, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.get_user_by_token(token)
    return {"username": user.username}


auth_service1 = AuthService(Depends(get_db))   

@app.get('/punchin')
def update_user_punchin(token:str=Depends(auth_service1.get_user_byheader),db:Session=Depends(get_db)):
    auth_service = AuthService(db)
    user=auth_service.get_user_by_token(token,db)
    id=user.id
    
    new_time_stamp=timestampuser(user_id=id,time=datetime.datetime.utcnow(),typeof=typeoff.INT)
    db.add(new_time_stamp)
    db.commit()
    db.refresh(new_time_stamp)
    

@app.get('/punchout')
def update_user_punchout(token:str=Depends(auth_service1.get_user_byheader),db:Session=Depends(get_db)):
    auth_service = AuthService(db)
    user=auth_service.get_user_by_token(token,db)
    id=user.id
    
    new_time_stamp=timestampuser(user_id=id,time=datetime.datetime.utcnow(),typeof=typeoff.OUT)
    db.add(new_time_stamp)
    db.commit()
    db.refresh(new_time_stamp)

@app.get('/getusertime')
def workinghours(username: str, db: Session = Depends(get_db)):
    punch_service = PunchService(db)
    return punch_service.get_user_working_hours(username)


@app.get('/admin/panel')
def all_details(db: Session = Depends(get_db)):
    punch_service = PunchService(db)
    return punch_service.get_all_user_details()
