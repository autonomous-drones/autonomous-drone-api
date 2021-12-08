import io
import os
import zipfile


def zip_files(file_paths, output_file):
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as z:
        for file in file_paths:
            file_name = os.path.basename(file)
            z.write(file, file_name)
        z.close()


def unzip_file(directory, zip_bytes):
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    z.extractall(directory)
    z.close()
