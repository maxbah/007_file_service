import os
import file_service

from typing import Tuple
from src.config import Config
from src.crypto import Encryption


class EncryptedFileService(file_service.FileService):
    def __init__(self, wrapped_file_service: file_service.FileService):
        self.wrapped_file_service = wrapped_file_service

    def read(self, filename: str) -> str:
        encryptor = Encryption.get_encryptor(filename)
        key_file_name = encryptor.key_file_name(filename)
        with open(key_file_name) as f:
            key = f.read()
        encrypted_data = self.wrapped_file_service.read(filename)
        decrypted_data = encryptor.decrypt(encrypted_data, key)
        return decrypted_data

    def write(self, data: str) -> str:
        encryption_type = Config().encryption_type()
        encryptor = Encryption.get_encryptor(encryption_type)
        encrypted_data, key = encryptor.encrypt(data)
        filename = self.wrapped_file_service.write(encrypted_data)
        key_file_name = encryptor.key_file_name(filename)
        with open(key_file_name) as f:
            f.write(key)
        return filename

    def ls(self) -> [str]:
        return self.wrapped_file_service.ls()

    def cd(self, dir: str) -> None:
        return self.wrapped_file_service.cd(dir)

    def remove(self, filename: str) -> None:
        self.wrapped_file_service.remove(filename)
        encryptor = Encryption.get_encryptor(filename)
        key_file_name = encryptor.key_file_name(filename)
        os.remove(key_file_name)

    def read_metadata(self, filename: str) -> Tuple[int, int, int]:
        return self.wrapped_file_service.read_metadata(filename)
