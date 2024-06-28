from passlib.context import CryptContext
from starlette import status
import models
from fastapi import FastAPI, Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas import user_register, user_login
from models import User, timestampuser, typeoff
import time


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: user_register):
        username = user.username
        existing_user = self.db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        password = user.password
        name = user.name
        hashed_password = bcrypt_context.hash(password)
        new_user = User(fullname=name, username=username, hashed_password=hashed_password)
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()