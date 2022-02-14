import os
from abc import ABCMeta, abstractmethod
from typing import Tuple

from src import utils
from src.crypto.signature import SignatureFactory
from src.utils import get_human_date
import logging


class FileService(metaclass=ABCMeta):

    @abstractmethod
    def read(self, filename : str) -> str: raise Exception("not implemented")

    @abstractmethod
    def write(self, data : str) -> str: raise Exception("not implemented")

    @abstractmethod
    def ls(self) -> [str]: raise Exception("not implemented")

    @abstractmethod
    def cd(self, dir : str) -> None: raise Exception("not implemented")

    @abstractmethod
    def remove(self, filename: str) -> None: raise Exception("not implemented")

    @abstractmethod
    def read_metadata(self, filename : str) -> Tuple[int, int, int]: raise Exception("not implemented")

# def read_file(filename: str) -> str:
#     """
#     Function to read file
#     :param filename: Name of file
#     :return: data
#     """
#     logging.info("Start read file")
#     with open(filename, "r") as f:
#         data = f.read()
#     return data
#
#
# def read_signed_file(filename: str) -> str:
#     data = read_file(filename)
#     for label in SignatureFactory.signers:
#         sig_file_name = f'{filename}.{label}'
#         if os.path.exists(sig_file_name):
#             signer = SignatureFactory.get_signer(label)
#             with open(sig_file_name, 'r') as sig_file:
#                 actual_data = signer(data)
#                 exp_data = sig_file.read()
#                 if actual_data == exp_data:
#                     print(f" Sign {filename} data: {data}")
#                     return data
#                 logging.error(f"actual_data != exp_data: {actual_data} != {exp_data}")
#
#
# def create_file(filename: str, content: str) -> None:
#     """
#     Write content to file
#     :param filename: name of file
#     :param content: content of file
#     """
#     logging.debug(f"Writing to: {filename}\nContent: {content}")
#     with open(filename, "w") as file:
#         file.write(content)
#
#
# def create(content: str) -> str:
#     """
#     Function to create new file with content and random filename
#     :param content: data to write into the file
#     :return: content
#     """
#     logging.info("Start file creation")
#     file_name = utils.random_file_name()
#     if os.path.exists(file_name):
#         raise Exception(f"{file_name} already existed")
#     create_file(file_name, content)
#     with open(file_name, "w") as f:
#         f.write(content)
#     print(f'File - {file_name} created. File content: {content}')
#     return file_name
#
#
# def create_signed_file(content: str, signer: str):
#     """
#     Create file with signature
#     :param content: file content
#     :param signer:  signer
#     :return: None
#     """
#     logging.info('Start creation file with sign')
#     filename = create(content)
#     sig_filename = f'{filename}.{signer}'
#     signer = SignatureFactory.get_signer(signer)
#     logging.info(f"Class signer type: {type(signer)}")
#     sig_content = signer(content)
#     create_file(sig_filename, sig_content)
#     return filename, sig_filename
#
#
# def delete_file(filename: str):
#     """
#     Function to delete file
#     :param filename: Name of file to delete
#     :return: Bool
#     """
#     logging.info("Start file deletion")
#     return os.remove(filename)
#
#
# def list_dir(path: str) -> list:
#     """
#     Function to get list dirs
#     :param path: path to directory
#     :return: listdir
#     """
#     logging.info("Start list dir")
#     return os.listdir(path)
#
#
# def change_dir(directory: str):
#     """
#     Function to change directory
#     :param directory: directory to change
#     :return: None
#     """
#     logging.info("Start ch dir")
#     return os.chdir(directory)
#
#
# def get_file_permissions(filename: str):
#     """
#     Function to get permission from filename
#     :param filename: File name
#     :return: None
#     """
#     logging.info("Start get fileperm")
#     if os.path.exists(filename):
#         permissions = os.stat(filename).st_mode
#         print(f"file permissions : {permissions}")
#     else:
#         print('File not existed')
#
#
# def set_file_permissions(filename: str, perm: int):
#     """
#     Function to set permission for filename
#     :param filename: Name of file
#     :param perm: permission value
#     :return: None
#     """
#     logging.info("Start set fileperm")
#     if os.path.exists(filename):
#         print(f"Set {perm} to {filename}")
#         os.chmod(filename, perm)
#     else:
#         print('File not existed')
#
#
# def get_cwd():
#     """
#     Function to get current directory
#     :return: current directory
#     """
#     logging.info("Start get cwd")
#     wd = os.getcwd()
#     return wd
#
#
# def get_file_metadata(filename: str) -> tuple:
#     """
#     Read file and get metadata
#     :param filename:
#     :return: tuple(create_date, modification_date, file_size)
#     :raises Exception ig file not exist
#     """
#     logging.info("Start get file metadata")
#     create_date = os.path.getctime(filename)
#     modification_date = os.path.getmtime(filename)
#     file_size = os.path.getsize(filename)
#     return get_human_date(create_date), get_human_date(modification_date), file_size
