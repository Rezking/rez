from fastapi import APIRouter ,Body, File , UploadFile, Depends,HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict
import jwt
from everyday_object_detection.Focus_mode import everydayobjectdetection
from faceRecognition.FR2 import face_recognition
from currency_identification.currency_detection import currency_detection
from OCR.ocr  import *
from pydantic import BaseModel, Field, EmailStr


users = [
    {
        "email":"onanugaoreoluwa@outlook.com",
        "password":"oreoluwa"
}
]
#run cmd openssl rand -hex 32 to generate new secret
JWT_SECRET = "24cf226033e98d804030c80bef1abcf1b91e14d13de4ffef34daa20eb19fe906"
JWT_ALGORITHM = "HS256"

class UserModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    
class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
def signJWT(user_id : str) -> Dict[str,str]:
    payload = {
        "user_id":user_id,
        "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            # time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithm = JWT_ALGORITHM)
        if decoded_token["exp"] >= datetime.utcnow():
            return decoded_token
        else: None
    except:return {}

    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


    
def token_response(token:str):
    return {
        "access_token": token
    }
    

Text_router = APIRouter()

users = []
def check_user(data: UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@Text_router.post("/signup/",tags=["user"])
async def create_user(user: UserModel = Body(...)):
    users.append(user)  #db call here
    return signJWT(user.email)

@Text_router.post("/user/login", tags=["user"])
async def user_login(user: UserLogin = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


ocr1 = OCR()

@Text_router.post("/abstract_mode/images/",tags = ["OCR"])
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # <-- Important!
    with open("temp.jpg", "wb") as f:
        f.write(contents)
    text = ocr1.text_detection('simple', "temp.jpg")
    return {"Text": text}

@Text_router.post("/document_mode/images/", tags = ["OCR"])
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # <-- Important!
    with open("temp.jpg", "wb") as f:
        f.write(contents)
    text = ocr1.text_detection('document', "temp.jpg")
    return {"Text": text}


@Text_router.post("/currency/images/",tags = ["currency"])
async def create_upload_file(file: UploadFile = Depends(JWTBearer())):
    contents = await file.read()  # <-- Important!
    with open("temp.jpg", "wb") as f:
        f.write(contents)
    path = 'currency_identification/model/best.pt'
    currency = currency_detection(path)
    text = currency.main_detection(path='temp.jpg')
    return {"Text": text}

@Text_router.post("/facereco/images/", tags = ["currency"])
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # <-- Important!
    with open("temp.jpg", "wb") as f:
        f.write(contents)
    threshold = 1
    database = "faceRecognition/database.npy"
    faceCascade= "faceRecognition/haarcascades/haarcascade_frontalface_default.xml"
    face_recog = face_recognition(threshold= threshold, haarcascades = faceCascade, database_exist = True, database_path = database)
    test_image_path = "temp.jpg"
    text = face_recog.face_detection(source = "image", path = test_image_path)
    return {"Text": text}

@Text_router.post("/focus/video/", tags = ["focus_mode"])
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # <-- Important!
    with open("temp.mp4", "wb") as f:
        f.write(contents)     
    detection = everydayobjectdetection(object_threshold = object_areas,show_video=True)
    width = 640  # video resolutions
    height = 480
    res = (width,height)
    text = detection.detect_object(videopath= vidpath, res = res)
    yield text
