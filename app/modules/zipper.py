"""Zip module"""
import io
import os
import zipfile


def zip_files(file_paths, output_file):
    """Zips files"""
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as w_zip:
        for file in file_paths:
            file_name = os.path.basename(file)
            w_zip.write(file, file_name)
        w_zip.close()


def unzip_file(directory, zip_bytes):
    """Unzips files"""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as u_zip:
        u_zip.extractall(directory)
        u_zip.close()
