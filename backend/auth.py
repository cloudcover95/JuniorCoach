from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "coach" or credentials.password != "juniorcoach2026":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username