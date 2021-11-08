import os
import secrets

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import FileResponse

app = FastAPI()

security = HTTPBasic()

save_path_json = 'uploads/json/'
save_path_img = 'uploads/img/'

def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "drone")
    correct_password = secrets.compare_digest(credentials.password, "drone")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
async def root():
    return {"message": "Autonomous Drone API"}

@app.post("/upload/json/")
async def create_upload_file(flightName: str, uploadedFile: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(authorize)):

    if(os.path.isdir(f"{save_path_json}{flightName}") == False):
         os.mkdir(f"{save_path_json}{flightName}")

    file_location = f"{save_path_json}{flightName}/{uploadedFile.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploadedFile.file.read())
    return {
        "message": f"File '{uploadedFile.filename}' was successfully saved in '{file_location}'"
    }

@app.post("/upload/img/")
async def create_upload_file(flightName: str, uploadedFile: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(authorize)):
    if (os.path.isdir(f"{save_path_img}{flightName}") == False):
        os.mkdir(f"{save_path_img}{flightName}")

    file_location = f"{save_path_json}{flightName}/{uploadedFile.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploadedFile.file.read())
    return {
         "message": f"File '{uploadedFile.filename}' was successfully saved in '{file_location}'"
    }

@app.get("/retrieve/json/")
async def read_items(flightName: str, recordId: int, credentials: HTTPBasicCredentials = Depends(authorize)):
    return FileResponse(
        path=f"uploads/json/{flightName}/record_{recordId}.json",
        filename=f"record_{recordId}.json",
        media_type='text/json'
        )

@app.get("/retrieve/img")
async def read_items(flightName: str, imageId: int, credentials: HTTPBasicCredentials = Depends(authorize)):
     return FileResponse(
        path=f"uploads/img/{flightName}/{imageId}_cam-image.jpg",
        filename=f"{imageId}_cam-image.jpg",
         media_type='image/jpeg'
        )