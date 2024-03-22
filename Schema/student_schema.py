from pydantic import BaseModel

class AddStudent(BaseModel):
    roll_no:str
    name:str
    class_name:str
    section:str
    

