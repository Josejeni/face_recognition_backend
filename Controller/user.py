from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Schema.user_schema import AddUserSchema,UpdateUserSchema,User
from Model.user_model import UserModel
from DataBase.db_connection import get_db
from Authentication import authentication

route=APIRouter(
    tags=['User'],
    prefix='/user'
)

@route.post('/login')
def getting_user(data:User,db:Session=Depends(get_db)):
   
    post=db.query(UserModel).filter(UserModel.user_name==data.username,UserModel.password==data.password).first()
    
    if post :
        token=authentication.create_token(post.user_name)
        post.token=token
        return {'data':post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")


@route.post('/add_user')
def create_user(data:AddUserSchema,db:Session=Depends(get_db)):
    print(data.dict())
    values=UserModel(**data.dict())
    print(values)
    db.add(values)
    db.commit()
    return HTTPException(status_code=200,detail="User Created Successfully")


@route.put("/update_record")
def updateRecord(data:UpdateUserSchema,db:Session=Depends(get_db),user=Depends(authentication.verify_token)):
    print(user)
    query=db.query(UserModel).filter(UserModel.user_name==user)
    values=query.first()
    if values:
        query.update(data.dict(), synchronize_session=False)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK,detail="Updated Successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

@route.delete("/delete_record/{id}")
def deleteRecord(id:int,db:Session=Depends(get_db)):
    try:
        query=db.query(UserModel).filter(UserModel.id==id)
        if not query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Found")
        else:
            query.delete()
            db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Found")


