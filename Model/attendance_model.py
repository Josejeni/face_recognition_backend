from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,TIMESTAMP,TIME,Date
from .student_model import Base

class AttendanceModel(Base):
    __tablename__='attendance_tbl'

    id=Column(Integer,primary_key=True)
    roll_no=Column(String,ForeignKey("student_tbl.roll_no",ondelete="CASCADE"),nullable=False)
    name=Column(String,nullable=False)
    date=Column(Date,nullable = False , server_default =func.now())
    time=Column(TIME,server_default=func.now())


# class EntryAttendanceModel(Base):
#     __tablename__='entryattendance_tbl'

#     id=Column(Integer,primary_key=True)
#     roll_no=Column(String,ForeignKey("student_tbl.roll_no",ondelete="CASCADE"),nullable=False)
#     name=Column(String,nullable=False)
#     date=Column(Date,nullable = False , server_default =func.now())
#     time=Column(TIME,server_default=func.now())

# class ExitAttendanceModel(Base):
#     __tablename__='attendance_tbl'

#     id=Column(Integer,primary_key=True)
#     roll_no=Column(String,ForeignKey("student_tbl.roll_no",ondelete="CASCADE"),nullable=False)
#     name=Column(String,nullable=False)
#     date=Column(Date,nullable = False , server_default =func.now())
#     time=Column(TIME,server_default=func.now())