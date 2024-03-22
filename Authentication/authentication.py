from jose import jwt , JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer


secret_key ='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
def create_token(user_name:str):
    data={"user_name":user_name,"exp":datetime.utcnow()+timedelta(minutes=30)}
    token=jwt.encode(data,secret_key,algorithm='HS256')
    print("token",token)
    return token

oauth_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

def verify_token(token:str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Unauthorized access')
    try:
        data = jwt.decode(token ,secret_key , algorithms='HS256')
        if data.get("user_name"):
            # print( data.get("user_name"))
            return data.get('user_name')
        
        if data.get("user_id") is None :
            raise credential_exception
        
        # token_data = tokenData(user_id=data.get("user_id") , role_id = data.get("role_id") , user_name= data.get('first_name'))
        # return token_data
    
    except JWTError as error:

        raise credential_exception
    
# def current_user(token:str):
#     # print(token)
#     # credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Unauthorized access')
#     data = verify_token(token)
#     return data 
    

# token=create_token()
# verify_token(token)
    

