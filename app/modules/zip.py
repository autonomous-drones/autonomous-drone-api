import io
import zipfile


def unzip_file(directory, zip_bytes):
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    z.extractall(directory)
    z.close()
