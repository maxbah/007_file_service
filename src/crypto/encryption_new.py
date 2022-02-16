import os
from abc import ABCMeta, abstractmethod
from random import Random
from typing import Tuple
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from src.config import Config
from src.crypto import SymmetricEncryption
from src.utils import random_string


class Encryption(metaclass=ABCMeta):
    label = ""
    encryptors = []

    def __init__(self):
        self.encryptors.append(self)

    @abstractmethod
    def encrypt(self, data: str) -> Tuple:
        """
        Encrypts data,
        generate new key for each data
        :param data: data to encrypt
        :return:  encrypted data and key to decrypt it
        """
        raise NotImplemented()

    @abstractmethod
    def decrypt(self, encrypted_data:str, key:str) -> str:
        """
        Decrypt data with provided key
        :param encrypted_data: data to decrypt
        :param key: decryption key
        :return: decrypted data
        """
        raise NotImplemented()

    @abstractmethod
    def key_file_match(self, key_file):
        raise NotImplemented()

    @abstractmethod
    def key_file_ext(self) -> str:
        raise NotImplemented()

    @staticmethod
    def get_encryptor_for_key_file(key_file):
        for encryptor in Encryption.encryptors:
            encryptor.key_file_match(key_file)

    @staticmethod
    def get_encryptor(filename):
        current_encryptor = None
        for encryptor in Encryption.__subclasses__():
            if os.path.exists(encryptor().key_name(filename)):
                if not current_encryptor:
                    current_encryptor = encryptor()
                else:
                    raise Exception("More than one encryptor is found!")
        if current_encryptor:
            return current_encryptor
        else:
            raise Exception("Encryptor is not found!")

    def key_name(self, filename):
        key_path = Config().key_path()
        return os.path.join(key_path, f"{filename}.{type(self).label}")

    @staticmethod
    def get_encryptor_by_label(label):
        for encryptor in Encryption.__subclasses__():
            if encryptor().label == label:
                return encryptor()


class SymetricEncryption(Encryption):
    label = "aes"

    def key_file_match(self, key_file: str):
        return key_file.endswith("aes")

    def key_file_name(self, filename: str):
        return os.path.join(filename, "aes")

    def encrypt(self, data):
        key = random_string(16).encode()
        aes = AES.new(key, AES.MODE_EAX)
        encrypted_data, tag = aes.encrypt_and_digest(data.encode())
        session_key = bytearray(aes.nonce)
        session_key.extend(bytearray(tag))
        session_key.extend(bytearray(key))
        return encrypted_data, session_key

    def decrypt(self, encrypted_data, session_key):
        n = 16
        session_key = bytearray(session_key)
        nonce, tag, session_key = [bytes(session_key[i:i + n]) for i in range(0, len(session_key), n)]
        aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = aes.decrypt_and_verify(encrypted_data, tag)
        return data.decode()


class HybridEncryption(Encryption):

    label = "hybrid"

    def __init__(self):
        self.symmetric_encryption = SymmetricEncryption()
        key_path = Config().key_path()
        self.key_path = os.path.join(key_path, "key.pem")
        self._rsa_key = None

    @property
    def rsa_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path) as key:
                self._rsa_key = RSA.import_key(key.read())
        else:
            random_generator = Random.new().read
            self._rsa_key = RSA.generate(1024, random_generator)
            with open(self.key_path, "w") as file:
                file.write(self._rsa_key.export_key("PEM").decode())
        return PKCS1_OAEP.new(self._rsa_key)

    def encrypt(self, data):
        encrypted_data, session_key = self.symmetric_encryption.encrypt(data)
        session_key = self.rsa_key.encrypt(session_key)
        return encrypted_data, session_key

    def decrypt(self, encrypted_data, session_key):
        session_key = self.rsa_key.decrypt(bytearray(session_key))
        data = self.symmetric_encryption.decrypt(encrypted_data, session_key)
        return data
