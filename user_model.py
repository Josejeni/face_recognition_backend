from sqlalchemy import Column , Integer , String ,Boolean ,BigInteger ,DateTime,func,ForeignKey
from DataBase.db_connection import Base

class UserModel(Base):
    __tablename__ = "user"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_name = Column(String,nullable = False)
    name = Column(String , nullable = False)
    password = Column (String , nullable = False)
    role = Column(Integer ,default=1 , nullable = False)
    created_at = Column(DateTime(timezone=True) , nullable = False , server_default =func.now())
    created_by=Column(String,nullable=True)

# class Config:
#         orm_mode = True