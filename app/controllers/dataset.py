"""Dataset Controller"""
import os
from typing import List
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBasicCredentials
from starlette import status
from starlette.responses import FileResponse
import app.config as c
from app.modules import auth, zipper, file_system


router = APIRouter()


@router.post("/upload/")
async def create_upload_files(flight_name: str, uploaded_files: List[UploadFile] = File(...),
                              credentials: HTTPBasicCredentials = Depends(auth.authorize)):
    """Multi file upload"""
    for input_file in uploaded_files:
        directory = f"{c.UPLOAD_DIR}/{flight_name}"

        if not os.path.isdir(directory):
            os.mkdir(directory)

        file_location = f"{directory}/{input_file.filename}"
        buffer = input_file.file.read()

        if("application/zip" and "application/x-zip-compressed") in input_file.content_type:

            zipper.unzip_file(directory, buffer)
        else:
            with open(file_location, "wb+") as file_object:
                file_object.write(buffer)

    return {"message": "Files uploaded successfully"}


@router.get("/retrieve/")
async def read_retrieve_files(
        flight_name: str,
        credentials: HTTPBasicCredentials = Depends(auth.authorize)
):
    """Retrieve multiple files as ZIP file"""
    if not os.path.isdir(f"{c.UPLOAD_DIR}/{flight_name}"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flight not found with name {flight_name}",
        )

    output_file_path = f"{c.COMPRESSED_DIR}/{flight_name}.zip"

    file_paths = file_system.get_file_paths(f"{c.UPLOAD_DIR}/{flight_name}/")
    zipper.zip_files(file_paths, output_file_path)

    return FileResponse(
        path=output_file_path,
        filename=os.path.basename(output_file_path),
        media_type="application/zip"
    )
