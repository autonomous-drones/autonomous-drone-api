import os
from typing import List

from fastapi import APIRouter
from fastapi import File, UploadFile, Depends
from fastapi.security import HTTPBasicCredentials
from starlette.responses import FileResponse

import app.config as c
import app.modules.auth as auth
from app.modules import zip

router = APIRouter()


@router.post("/upload/")
async def create_upload_files(flightName: str, uploadedFiles: List[UploadFile] = File(...),
                              credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    for uploadedFile in uploadedFiles:
        if not os.path.isdir(f"{c.save_path_json}{flightName}"):
            os.mkdir(f"{c.save_path_json}{flightName}")

        directory = f"{c.save_path_json}{flightName}/"
        file_location = f"{directory}/{uploadedFile.filename}"
        buffer = uploadedFile.file.read()

        if uploadedFile.content_type == "application/zip":
            zip.unzip_file(directory, buffer)
        else:
            with open(file_location, "wb+") as file_object:
                file_object.write(buffer)

    return {
        "message": "Files uploaded successfully"
    }


@router.get("/retrieve/json/")
async def read_items(flightName: str, recordId: int, credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    return FileResponse(
        path=f"uploads/json/{flightName}/record_{recordId}.json",
        filename=f"record_{recordId}.json",
        media_type='text/json'
    )


@router.get("/retrieve/img")
async def read_items(flightName: str, imageId: int, credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    return FileResponse(
        path=f"uploads/img/{flightName}/{imageId}_cam-image.jpg",
        filename=f"{imageId}_cam-image.jpg",
        media_type='image/jpeg'
    )
