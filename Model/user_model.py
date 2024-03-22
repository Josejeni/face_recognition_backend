from sqlalchemy import Column,String,Integer,BigInteger
from .attendance_model import Base

class UserModel(Base):
    __tablename__='user_tbl'

    id=Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name=Column(String,nullable=False)
    user_name=Column(String,nullable=False)
    password=Column(String,nullable=False)
    mobile_no=Column(BigInteger,nullable=False)
    role=Column(Integer,default=2)