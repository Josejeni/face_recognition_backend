from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from DataBase.db_connection import get_db,session_local
from Model.student_model import StudentModel
from Model.attendance_model import AttendanceModel
from Authentication.authentication import verify_token
import face_recognition
import cv2
import numpy as np
from sqlalchemy import desc
import threading
from datetime import datetime,time,timedelta
import csv,os


route=APIRouter(
    tags=['Attendance'],
    prefix='/attendance'
)

known_faces_names=[]
known_face_encoding=[]
video_capture=cv2.VideoCapture(0)
face_encoding=[]
face_names=[]

# s =True


def load_data_from_db():
    print("yess")
    db = session_local()
    try:
        data = db.query(StudentModel).all()
        return data
    finally:
        db.close()


def create_encode():

    posts=load_data_from_db()
    for post in posts:
        known_faces_names.append(post.roll_no)
        # temp=post.roll_no 
        print("post.img_path",post.img_path)
        key=face_recognition.load_image_file(post.img_path)
        temp=face_recognition.face_encodings(key)[0]
        known_face_encoding.append(temp)

create_encode()

@route.post('/add_attendance')
async def post_attendance(  db:Session=Depends(get_db)):
    now=datetime.now()
    current_date=now.strftime("%Y-%m-%d ") 
    filename = 'Attendance Sheet- ' + current_date + '.csv'
    lnwriter=''
    # Check if file exists
    if os.path.exists(filename):
        mode = 'a+'  # Open existing file for appending
        f=open('Attendance Sheet- '+current_date+'.csv',mode,newline='')
        lnwriter=csv.writer(f)
    else:
        # mode = 'w+'  # Create new file if it doesn't exist
        f=open('Attendance Sheet- '+current_date+'.csv','w+',newline='')



        lnwriter=csv.writer(f)
        fieldnames=["Frds Name","Current Time"]
    # lnwriter.writerow(["Frds Name","Current Time"])
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    copied_rollno=known_faces_names.copy()
    if not video_capture.isOpened():
        return {'error': 'Failed to open camera'}

    while True:
    # Grab a single frame of video
        ret, frame = video_capture.read()
    
        if not ret:
            return {'error': 'Failed to read frame from camera'}

    # Convert the image from BGR color to RGB color
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            # Compare face encoding with known face encodings
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding,tolerance=0.6)
            face_distance=face_recognition.face_distance(known_face_encoding,face_encoding)
            current_date = datetime.now().strftime("%Y/%m/%d")
            best_match_index=np.argmin(face_distance)
            if matches[best_match_index]:
                current_time=now.strftime("%I:%M:%S %p")
                roll_no=known_faces_names[best_match_index]
                if roll_no in copied_rollno:
                    stdudent_details = db.query(StudentModel).filter(StudentModel.roll_no == roll_no).first()
                    print("student",stdudent_details)
                    if(stdudent_details):
                        data = AttendanceModel(roll_no=roll_no, name=stdudent_details.name)
                        db.add(data)
                        db.commit()
                        print(f"Attendance recorded for {stdudent_details.name}")
                        lnwriter.writerow([stdudent_details.name,current_time])
                        copied_rollno.remove(roll_no)
            else:
                print("Not Matched")
        # Show the processed frame
        cv2.imshow("Attendance System", frame)
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break
    f.close()
    cv2.destroyAllWindows()
    
    print("quited.....")
    return {'message': 'Camera closed successfully'}



@route.get('/get_attendance')
def getting_attendance(db:Session=Depends(get_db),user=Depends(verify_token)):
    posts=db.query(AttendanceModel).order_by(desc(AttendanceModel.id)).all()
    return posts


