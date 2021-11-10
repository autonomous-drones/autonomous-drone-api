import io
import zipfile


def unzip_file(directory, bytes):
    z = zipfile.ZipFile(io.BytesIO(bytes))
    z.extractall(directory)
    z.close()
