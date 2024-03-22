from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
# from sqlalchemy.ext.declarative import 
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
import cv2
import numpy as np
import os

app = FastAPI()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/Sample1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students_s"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    entry_time = Column(DateTime)
    exit_time = Column(DateTime, nullable=True)
    period = Column(Integer)

# Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def process_camera():
    global background_tasks
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = detect_faces(frame)
        if len(faces) > 0:
            background_tasks.add_task(record_attendance, faces,frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

background_tasks = BackgroundTasks()

def record_attendance(faces, frame,period=1):
    with get_db() as db:
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            student_id = 1  # Dummy student_id for demonstration
            attendance = Attendance(student_id=student_id, entry_time=datetime.now(), period=period)
            db.add(attendance)
            db.commit()

def calculate_attendance():
    with get_db() as db:
        total_students = db.query(func.count(Student.id)).scalar()
        attendance_data = {}
        for period in range(1, 9):  # Assuming 8 periods
            period_attendance = {}
            total_attendance = db.query(func.count(Attendance.id)).filter(Attendance.period == period).scalar()
            period_attendance["total_attendance"] = total_attendance
            period_attendance["attendance_percentage"] = (total_attendance / total_students) * 100
            attendance_data[period] = period_attendance
        return attendance_data

@app.get("/start_camera/")
async def start_camera():
    global background_tasks
    background_tasks.add_task(process_camera)
    return {"message": "Camera feed processing started."}

@app.get("/stop_camera/")
async def stop_camera():
    global background_tasks
    os.system("taskkill /im python.exe /f")  # Terminate Python process to stop camera feed processing
    return {"message": "Camera feed processing stopped."}

@app.get("/attendance/")
async def get_attendance():
    attendance_data = calculate_attendance()
    return attendance_data
