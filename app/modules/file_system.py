"""Filesystem module"""
import os


def get_file_paths(directory):
    """Get file paths"""
    file_paths = []

    for files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(directory, filename)
            file_paths.append(file_path)

        return file_paths
