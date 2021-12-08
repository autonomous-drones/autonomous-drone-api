import os
from typing import List

from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBasicCredentials
from starlette import status
from starlette.responses import FileResponse

import app.config as c
import app.modules.auth as auth
import app.modules.zip as zip
import app.modules.file_system as file_system

router = APIRouter()


@router.post("/upload/")
async def create_upload_files(flightName: str, uploadedFiles: List[UploadFile] = File(...),
                              credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    for uploadedFile in uploadedFiles:
        directory = f"{c.upload_directory}/{flightName}"

        if not os.path.isdir(directory):
            os.mkdir(directory)

        file_location = f"{directory}/{uploadedFile.filename}"
        buffer = uploadedFile.file.read()

        if uploadedFile.content_type == "application/zip" or uploadedFile.content_type == "application/x-zip-compressed":
            zip.unzip_file(directory, buffer)
        else:
            with open(file_location, "wb+") as file_object:
                file_object.write(buffer)

    return {"message": "Files uploaded successfully"}


@router.get("/retrieve/")
async def read_retrieve_files(flightName: str, credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    if not os.path.isdir(f"{c.upload_directory}/{flightName}"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flight not found with name {flightName}",
        )

    output_file_path = f"{c.compressed_directory}/{flightName}.zip"

    file_paths = file_system.get_file_paths(f"{c.upload_directory}/{flightName}/")
    zip.zip_files(file_paths, output_file_path)

    return FileResponse(
        path=output_file_path,
        filename=os.path.basename(output_file_path),
        media_type="application/zip"
    )
