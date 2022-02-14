import os
from abc import ABCMeta, abstractmethod
from random import Random
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from src.config import Config
from src.utils import random_string

class Encryption(metaclass=ABCMeta):
    @abstractmethod
    def encrypt(self, data : str) -> Tuple[str, str]:
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


    @staticmethod
    def get_encryptor(self, filename):
        # Ask all encryptors if they are able to find apropriate keys for this file
        pass

class SymetricEncryption(Encryption):
   def encrypt(self, data) -> Tuple[str, str]:
       session_key = random_string(10).encode()
       aes = AES.new(session_key, AES.MODE_EAX)
       encrypted_data, tag = aes.encrypt_and_digest(data.encode())
       return encrypted_data, f"{session_key},{tag},{aes.nonce}"

   def decrypt(self, encrypted_data:str, key:str) -> str:
       session_key, tag, nonce = key.split(",")
       aes = AES.new(session_key, AES.MODE_EAX, nonce)
       data = aes.decrypt_and_verify(encrypted_data, tag)
       return data


class HybrydEncryption(Encryption):

    def __init__(self):
        self.symetric_encryption = SymetricEncryption()
        keys_path = Config().keys_path()
        keys_path = os.path.join(keys_path, "key.pem")
        if os.path.exists(keys_path):
            self.rsa_key = RSA.import_key(open(keys_path).read())
        else:
            random_generator = Random.new().read
            self.rsa_key = RSA.generate(1024, random_generator)  # generate public and private keys
            open(keys_path).write(self.rsa_key.export_key('PEM'))

   def encrypt(self, data) -> Tuple[str, str]:
       encrypted_data, symetric_key = self.symetric_encryption.encrypt(data)
       encrypted_key= self.rsa_key.publickey.encrypt(symetric_key, 32)
       return  encrypted_data, encrypted_key

   def decrypt(self, encrypted_data:str, encrypted_key:str) -> str:
        symetric_key = self.rsa_key.decrypt(encrypted_key)
        data = self.symetric_encryption.decrypt(encrypted_data, symetric_key)
        return data