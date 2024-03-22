from fastapi import FastAPI,Depends,HTTPException,status
from Model.student_model import StudentModel
# from root_path.user_schema import User,Updatuser
from sqlalchemy.orm import Session
from DataBase.db_connection import session_local
from user_model import UserModel
from Model.user_model import Base
from DataBase.db_connection import engine
from datetime import datetime, timedelta
from Authentication.authentication import verify_token
from Controller import user,student,attendance
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
        data = db.query(StudentModel).all()
        return data
    finally:
        db.close()


app=FastAPI()
app.include_router(user.route)
app.include_router(student.route)
app.include_router(attendance.route)

app.add_middleware(
    CORSMiddleware,
    allow_origins =['*'],
    allow_methods = ['*'],
    allow_headers = ['*']
)




@app.get('/')
def sample():
    print("Hlo")
    
    return {'data':'hii'}

