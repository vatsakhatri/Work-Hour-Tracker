from passlib.context import CryptContext
from starlette import status
import models
from fastapi import FastAPI, Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas import user_register, user_login
from models import User, timestampuser, typeoff
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
import time

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class AuthService:
    
    def __init__(self, db: Session):
        self.db = db

    
    def authenticate_user(self, username1: str, password: str):
        user_from_db = self.db.query(User).filter(User.username == username1).first()
        if not user_from_db:
            return False
        if bcrypt_context.verify(password, user_from_db.hashed_password):
            return user_from_db
        return False

    def create_jwt(self, username: str):
        payload = {"username": username, "exp": time.time() + 60 * 60 * 24}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def get_user_by_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('username')
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            user = self.db.query(User).filter(User.username == username).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return user
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    def get_user_byheader(self,request:Request):
        auth=request.headers.get('Authorization')
        if not auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="no auth header") ;
        bearer=auth.split()[-1]
        user=self.get_user_by_token(bearer)
        if user:
            return bearer
