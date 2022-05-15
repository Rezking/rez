import time
from typing import Dict
import jwt

#run cmd openssl rand -hex 32 to generate new secret
JWT_SECRET = "24cf226033e98d804030c80bef1abcf1b91e14d13de4ffef34daa20eb19fe906"
JWT_ALGORITHM = "HS256"

def token_response(token:str):
    return {
        "access_token": token
    }
    
#To sign jwt
def signJWT(user_id : str) -> Dict[str,str]:
    payload = {
        "user_id":user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithm = JWT_ALGORITHM)
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else: None
    except:return {}
    


