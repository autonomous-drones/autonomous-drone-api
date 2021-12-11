"""Auth module"""
import secrets
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
import app.config as c

app = FastAPI()
security = HTTPBasic()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    """Authorize"""
    correct_username = secrets.compare_digest(credentials.username, c.CREDENTIALS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, c.CREDENTIALS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
