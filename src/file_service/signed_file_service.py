
import os
import logging
from .file_services import FileService
from typing import Tuple
from src.crypto import SignatureFactory


class SignedFileService(FileService):
    def __init__(self, wrapped_file_service):
        self.wrapped_file_service = wrapped_file_service

    def write(self, content: str, signer: str):
        """
        Create file with signature
        :param content: file content
        :param signer:  signer
        :return: None
        """
        logging.info('Start creation file with sign')
        filename = self.wrapped_file_service.create(content)
        sig_filename = f'{filename}.{signer}'
        signer = SignatureFactory.get_signer(signer)
        logging.info(f"Class signer type: {type(signer)}")
        sig_content = signer(content)
        self.wrapped_file_service.create_file(sig_filename, sig_content)
        return filename, sig_filename

    def read(self, filename: str) -> str:
        data = self.wrapped_file_service.read_file(filename)
        for label in SignatureFactory.signers:
            sig_file_name = f'{filename}.{label}'
            if os.path.exists(sig_file_name):
                signer = SignatureFactory.get_signer(label)
                with open(sig_file_name, 'r') as sig_file:
                    actual_data = signer(data)
                    exp_data = sig_file.read()
                    if actual_data == exp_data:
                        print(f" Sign {filename} data: {data}")
                        return data
                    logging.error(f"actual_data != exp_data: {actual_data} != {exp_data}")

    def ls(self):
        return self.wrapped_file_service.ls()

    def cd(self, directory: str):
        return self.wrapped_file_service.cd(directory)

    def remove(self, filename: str):
        self.wrapped_file_service.remove(filename)
        signer = SignatureFactory.get_signer(filename)
        sig_filename = signer.sig_filename(filename)
        self.wrapped_file_service.remove(sig_filename)

    def read_metadata(self, filename: str) -> Tuple[int, int, int]:
        return self.wrapped_file_service.read_metadata(filename)
