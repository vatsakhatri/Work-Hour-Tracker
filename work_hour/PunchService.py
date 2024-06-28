from sqlalchemy import extract
from starlette import status
import models
from fastapi import FastAPI, Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from schemas import user_register, user_login
from models import User, timestampuser, typeoff
import time
import datetime

class PunchService:
    def __init__(self, db: Session):
        self.db = db

    def punch_in(self, user_id: int):
        new_time_stamp = timestampuser(user_id=user_id, time=datetime.datetime.utcnow(), typeof=typeoff.INT)
        self.db.add(new_time_stamp)
        self.db.commit()
        self.db.refresh(new_time_stamp)
        return new_time_stamp

    def punch_out(self, user_id: int):
        new_time_stamp = timestampuser(user_id=user_id, time=datetime.datetime.utcnow(), typeof=typeoff.OUT)
        self.db.add(new_time_stamp)
        self.db.commit()
        self.db.refresh(new_time_stamp)
        return new_time_stamp

    def get_user_working_hours(self, username: str):
        now = datetime.datetime.utcnow()
        users = self.db.query(User, timestampuser).filter(User.id == timestampuser.user_id).filter(User.username == username).filter(extract('day', timestampuser.time) == now.day).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        time_data = [{"Time": time.time, "Tag": time.typeof} for user, time in users]
        zero = datetime.timedelta(0)
        i = 0
        while i < len(time_data):
            intime = time_data[i]["Time"]
            if i + 1 < len(time_data):
                outime = time_data[i + 1]["Time"]
            totaltime = outime - intime
            zero = zero + totaltime
            i = i + 2
        
        total_seconds = int(zero.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        return {"username": username, "total_working_hours": total_time_str}

    def get_all_user_details(self):
        now = datetime.datetime.utcnow()
        all_user_details = self.db.query(User, timestampuser).filter(User.id == timestampuser.user_id).all()
        if not all_user_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user details found")
        
        user_data = [{"username": user.username, "time": time.time, "type": time.typeof} for user, time in all_user_details]
        return user_data