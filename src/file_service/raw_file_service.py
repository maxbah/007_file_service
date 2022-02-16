import logging
import os
from src import utils

from src.file_service.file_services import FileService


class RawFileService(FileService):
    def __init__(self, workdir="."):
        self.workdir = workdir

    def read(self, filename: str) -> str:
        """
        Function to read file
        :param filename: Name of file
        :return: data
        """
        logging.info("Start read file")
        with open(filename, "r") as f:
            data = f.read()
        return data

    def write(self, content: str) -> None:
        """
        Write content to file
        :param content: content of file
        """
        filename = utils.random_file_name()
        logging.debug(f"Writing to: {filename} \nContent: {content}")
        with open(filename, "w") as file:
            file.write(content)
        return filename

    def create(self, content: str) -> str:
        """
        Function to create new file with content and random filename
        :param content: data to write into the file
        :return: content
        """
        logging.info("Start file creation")
        file_name = utils.random_file_name()
        if os.path.exists(file_name):
            raise Exception(f"{file_name} already existed")
        with open(file_name, "w") as f:
            f.write(content)
        print(f'File - {file_name} created. File content: {content}')
        return file_name

    def remove(self, filename: str) -> None:
        """
        Function to delete file
        :param filename: Name of file to delete
        :return: Bool
        """
        logging.info("Start file deletion")
        return os.remove(filename)

    def ls(self) -> list:
        """
        Function to get list dirs of curent directory
        :return: listdir
        """
        logging.info("Start list dir")
        return os.listdir()

    def cd(self, dir: str):
        """
        Function to change directory
        :param directory: directory to change
        :return: None
        """
        logging.info("Start ch dir")
        return os.chdir(dir)

    def get_file_permissions(self, filename: str):
        """
        Function to get permission from filename
        :param filename: File name
        :return: None
        """
        logging.info("Start get fileperm")
        if os.path.exists(filename):
            permissions = os.stat(filename).st_mode
            print(f"file permissions : {permissions}")
        else:
            print('File not existed')

    def set_file_permissions(self, filename: str, perm: int):
        """
        Function to set permission for filename
        :param filename: Name of file
        :param perm: permission value
        :return: None
        """
        logging.info("Start set fileperm")
        if os.path.exists(filename):
            print(f"Set {perm} to {filename}")
            os.chmod(filename, perm)
        else:
            print('File not existed')

    def get_cwd(self):
        """
        Function to get current directory
        :return: current directory
        """
        logging.info("Start get cwd")
        wd = os.getcwd()
        return wd

    def read_metadata(self, filename: str) -> tuple:
        """
        Read file and get metadata
        :param filename:
        :return: tuple(create_date, modification_date, file_size)
        :raises Exception ig file not exist
        """
        logging.info("Start get file metadata")
        create_date = os.path.getctime(filename)
        modification_date = os.path.getmtime(filename)
        file_size = os.path.getsize(filename)
        return utils.get_human_date(create_date), utils.get_human_date(modification_date), file_size
