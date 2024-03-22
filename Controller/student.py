from fastapi import APIRouter,Depends,File,UploadFile,HTTPException,status,Form
from sqlalchemy.orm import Session
from Schema.student_schema import AddStudent
from DataBase.db_connection import get_db
from typing import List,Optional,Union
import os 
import shutil
from Model.student_model import StudentModel
from fastapi.responses import FileResponse
import face_recognition
from Authentication.authentication import verify_token
from sqlalchemy import func

from Controller.attendance import known_faces_names,known_face_encoding


route=APIRouter(
    tags=["Student"],
    prefix="/student"
)


root_path='Assets\StudentImgs'

@route.post('/add_student')
def create_student(roll_no:str=Form(),year:str=Form(),dept:str=Form(),name:str=Form(),file: UploadFile = File(...),db:Session=Depends(get_db)):
    print(file.filename,roll_no,dept+year)
    student=db.query(StudentModel).filter(StudentModel.roll_no==roll_no).first()
    if not student:
        file_path=f"{root_path}\{dept+year}"
        # file_path=os.path.join(root_path,class_name)
        print(file_path)
        try:
            os.makedirs(file_path)
        except:
            pass
        with open(f"{file_path}\{file.filename}","wb") as buffer:    
            shutil.copyfileobj(file.file,buffer)
        location=os.path.join(file_path,file.filename)
        post=StudentModel(roll_no=roll_no,dept=dept,year=year,name=name,img_path=location)
        db.add(post)
        db.commit()
        known_faces_names.append(name)
        temp=post.name 
        print("post.img_path",location)
        key=face_recognition.load_image_file(location)

        # key=face_recognition.load_image_file(f"E:\Jose\Python_Poc\Assets\StudentImgs\c12\j.png")
        temp=face_recognition.face_encodings(key)[0]
        known_face_encoding.append(temp)
        return {"data":"Created successfully"}  
    return {"data":"Already excised"}

@route.get("/student_image/{id}")
def getting_img(id:str,db:Session=Depends(get_db)):
    post=db.query(StudentModel).filter(StudentModel.roll_no==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="Not found")
    print(post.img_path)
    return FileResponse(post.img_path)    


@route.get('/student_search/{values}')
def search(values:str,db:Session=Depends(get_db)):
    print("yes",values)
    posts=db.query(StudentModel).filter(func.upper(StudentModel.name).contains(values.upper())).all()
    if posts:
        for post in posts:
            post.img_url='http://127.0.0.1:8000/student/student_image/'+post.roll_no
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="Not found")

@route.get('/get_stdents')
def getting_students(db:Session=Depends(get_db),user=Depends(verify_token)):
    posts=db.query(StudentModel).all()
    for post in posts:
        post.img_url='http://127.0.0.1:8000/student/student_image/'+post.roll_no
    return posts

@route.delete('/delete_student/{id}')
def delete_student(id:str,db:Session=Depends(get_db)):
    post=db.query(StudentModel).filter(StudentModel.roll_no==id)
    data=post.first() 
    print(data)  
    if data: 
        location=data.img_path
        post.delete(synchronize_session=False)
        db.commit()

        try: 
            os.remove(f"{location}") 
            return{"msg":"image deleted"}

        except OSError as error:
            return error
    return {"msg":'Deleted Successfully'}
    
    