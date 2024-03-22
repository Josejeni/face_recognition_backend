from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


try:
    sql_url = f"postgresql://postgres:postgres@localhost:5432/FaceRecognition"
    engine = create_engine(sql_url)
    session_local = sessionmaker(autocommit=False , autoflush=False ,expire_on_commit=False , bind=engine)
    print("connected")
except Exception as error:
    print("Error : ",error)
    
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()   
