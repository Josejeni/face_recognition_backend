from pydantic import BaseModel

class AddUserSchema(BaseModel):
    user_name:str
    password:str
    name:str
    mobile_no:int
    
class UpdateUserSchema(BaseModel):
    user_name:str
    password:str
    name:str
    mobile_no:int

class User(BaseModel):
    username: str
    password: str