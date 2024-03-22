from sqlalchemy import Column,String,Integer
from DataBase.db_connection import Base 

class StudentModel(Base):
    __tablename__='student_tbl'

    name=Column(String,nullable=False)
    roll_no=Column(String,nullable=False,primary_key=True)
    year=Column(String,nullable=False)
    dept=Column(String,nullable=False)
    img_path=Column(String,nullable=False)

