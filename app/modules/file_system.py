import os


def get_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(directory, filename)
            file_paths.append(file_path)

        return file_paths
