from pydantic import BaseModel

class user_register(BaseModel):
    name:str
    username:str
    password:str
    
class user_login(BaseModel):
    username:str
    password:str