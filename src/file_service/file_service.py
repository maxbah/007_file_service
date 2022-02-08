import os
from src import utils
from datetime import datetime


def read_file(filename: str) -> str:
    """
    Function to read file
    :param filename: Name of file
    :return: data
    """
    with open(filename, "r") as f:
        data = f.read()
    return data


def create_file(content: str) -> str:
    """
    Function to create new file with content and random filename
    :param content: data to write into the file
    :return: content
    """
    file_name = utils.random_file_name()
    if os.path.exists(file_name):
        create_file(content)
        return ''
    with open(file_name, "w") as f:
        f.write(content)
    print(f'File - {file_name} created. File content: {content}')
    return content


def delete_file(filename: str):
    """
    Function to delete file
    :param filename: Name of file to delete
    :return: Bool
    """
    return os.remove(filename)


def list_dir(path: str) -> list:
    """
    Function to get list dirs
    :param path: path to directory
    :return: listdir
    """
    return os.listdir(path)


def change_dir(directory: str):
    """
    Function to change directory
    :param directory: directory to change
    :return: None
    """
    return os.chdir(directory)


def get_file_permissions(filename: str):
    """
    Function to get permission from filename
    :param filename: File name
    :return: None
    """
    if os.path.exists(filename):
        permissions = os.stat(filename).st_mode
        print(f"file permissions : {permissions}")
    else:
        print('File not existed')


def set_file_permissions(filename: str, perm: int):
    """
    Function to set permission for filename
    :param filename: Name of file
    :param perm: permission value
    :return: None
    """
    if os.path.exists(filename):
        print(f"Set {perm} to {filename}")
        os.chmod(filename, perm)
    else:
        print('File not existed')


def get_cwd():
    """
    Function to get current directory
    :return: current directory
    """
    wd = os.getcwd()
    return wd


def get_file_metadata(filename: str) -> tuple:
    """
    Read file and get metadata
    :param filename:
    :return: tuple(create_date, midification_date, filesize)
    :raises Exception ig file not exist
    """
    create_date = os.path.getctime(filename)
    create_date_human = datetime.fromtimestamp(create_date).strftime("%b %d %Y %H:%M:%S")

    modification_date = os.path.getmtime(filename)
    modification_date_human = datetime.fromtimestamp(modification_date).strftime("%b %d %Y %H:%M:%S")
    f_size = os.path.getsize(filename)
    return (create_date_human, modification_date_human, f_size),
