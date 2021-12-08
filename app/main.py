import os
import secrets

from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import FileResponse

from app.modules import zip
from app.modules import file_system

app = FastAPI()
security = HTTPBasic()

upload_directory = 'uploads'
compressed_directory = 'compressed'


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


@app.post("/upload/")
async def create_upload_files(flightName: str, uploadedFiles: List[UploadFile] = File(...),
                              credentials: HTTPBasicCredentials = Depends(authorize)):
    for uploadedFile in uploadedFiles:
        directory = f"{upload_directory}/{flightName}"

        if not os.path.isdir(directory):
            os.mkdir(directory)

        file_location = f"{directory}/{uploadedFile.filename}"
        buffer = uploadedFile.file.read()

        if uploadedFile.content_type == "application/zip":
            zip.unzip_file(directory, buffer)
        else:
            with open(file_location, "wb+") as file_object:
                file_object.write(buffer)

    return {"message": "Files uploaded successfully"}


@app.get("/retrieve/")
async def read_retrieve_files(flightName: str, credentials: HTTPBasicCredentials = Depends(authorize)):
    if not os.path.isdir(f"{upload_directory}/{flightName}"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flight not found with name {flightName}",
        )

    output_file_path = f"{compressed_directory}/{flightName}.zip"

    file_paths = file_system.get_file_paths(f"{upload_directory}/{flightName}/")
    zip.zip_files(file_paths, output_file_path)

    return FileResponse(
        path=output_file_path,
        filename=os.path.basename(output_file_path),
        media_type="application/zip"
    )
