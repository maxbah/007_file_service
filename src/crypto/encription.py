import logging
from abc import ABCMeta, abstractmethod
from typing import Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Encryption(metaclass=ABCMeta):

    @abstractmethod
    def encrypt(self, data: str) -> Tuple[str, str]:
        """
        Encrypts data,
        generate new key for each data
        :param data: data to encrypt
        :return:  encrypted data and key to decrypt it
        """
        raise NotImplemented()

    @abstractmethod
    def decrypt(self, encrypted_data: str, key: str) -> str:
        """
                Decrypt data with provided key
                :param encrypted_data: data to decrypt
                :param key: decryption key
                :return: decrypted data
                """
        raise NotImplemented()


class SymmetricEncryption(Encryption):
    def __init__(self):
        self.key = Fernet.generate_key()
        self.f_key = Fernet(self.key)

    def encrypt(self, data: str) -> Tuple:
        """
         Data Encryption
        :param data: str
        :return: tuple
        """
        logging.info("Start data encryption ")
        b_data = str.encode(data)
        encrypted_data = self.f_key.encrypt(b_data)
        print("Original data: ", data, "\nEncrypted data: ", type(encrypted_data), encrypted_data,
              "\nf_key: ", self.f_key, "\nKey", self.key)
        res = encrypted_data, self.f_key
        return res

    def decrypt(self, encrypted_data: bytes, f_key) -> str:
        """
        Decryption data
        :param encrypted_data: str
        :param f_key: fernet_key
        :return: str
        """
        logging.info("Start data decryption ")
        f_key = self.f_key
        decrypted_data = f_key.decrypt(encrypted_data).decode()
        print("Encrypted data: ", encrypted_data, "\nDecrypted data: ", decrypted_data)
        return decrypted_data


class AsymmetricEncryption(Encryption):
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def storing_private_key_to_file(self, filename: str):
        """
        Write private key to filename
        :param filename: file name
        :return: str
        """
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        # create_file(f'{filename}.pem', pem)
        with open(f'{filename}.pem', 'wb') as f:
            f.write(pem)
        return filename

    def storing_public_key_to_file(self, filename: str):
        """
         Write publice key to filename
         :param filename: file name
         :return: str
         """
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # create_file(f'{filename}.pem', pem)
        with open(f'{filename}.pem', 'wb') as f:
            f.write(pem)
        return filename

    def reading_private_key(self, filename: str):
        """
        Reed private key from file
        :param filename: file name
        :return: key
        """
        with open(f'{filename}.pem', "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
            return private_key

    def reading_public_key(self, filename: str):
        """
        Reed public key from file
        :param filename: file name
        :return: key
        """
        with open(f'{filename}.pem', "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    def encrypt(self, symmetric_key: bytes) -> bytes:
        """
        Encrypt symmetric key with asymmetric public key
        :param symmetric_key: bytes
        :return: bytes
        """
        encrypted_symmetric_key = self.public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_symmetric_key

    def decrypt(self, encrypted_symmetric_key: bytes, private_key) -> bytes:
        """
        Decrypt symmetric key with asymmetric private key
        :param encrypted_symmetric_key: bytes
        :param private_key: key
        :return: bytes
        """
        private_key = self.private_key
        decrypted_symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_symmetric_key

# sym_enc = SymmetricEncryption()
# data_to_symmetric_encription = "Very security data blabla"
# print("Data to symmetric encryption: ", data_to_symmetric_encription)
# symmetric_key = sym_enc.generate_keys()
# print("Generated symmetric key:", symmetric_key)
# symmetric_encrypted_data = sym_enc.encrypt(data_to_symmetric_encription)
# print("___________________________")
# print("symmetric encrypted data:", symmetric_encrypted_data)
# print("___________________________")
# symmetric_decrypted_data = sym_enc.decrypt(*sym_enc.encrypt(data_to_symmetric_encription))
# print("symmetric decrypted data:", symmetric_decrypted_data)
#
# asym_enc = AsymmetricEncryption()
# print("symmetric key to asymmetric encription: ", symmetric_key)
# private_key, public_key = asym_enc.generate_keys()
# print("Generated asymmetric private key:", private_key)
# print("Generated asymmetric public key:", public_key)
# private_key_filename = asym_enc.storing_private_key_to_file('private_key')
# print("Storing asymmetric private key to 'private_key.pem':", private_key_filename)
# public_key_filename = asym_enc.storing_public_key_to_file('public_key')
# print("Storing asymmetric public key to 'public_key.pem':", public_key_filename)
# reading_private_key = asym_enc.reading_private_key(private_key_filename)
# print("Reading private key from 'private_key.pem':", reading_private_key,'==\n', private_key)
# reading_public_key = asym_enc.reading_public_key(public_key_filename)
# print("Reading public key from 'public_key':", reading_public_key, '==\n', public_key)
# asymmetric_encrypted_symmetric_key = asym_enc.encrypt(symmetric_encrypted_data[0])
# print("Asymmetric encrypt symmetric key:", asymmetric_encrypted_symmetric_key)
# asymmetric_decrypted_symmetric_key = asym_enc.decrypt(asymmetric_encrypted_symmetric_key, private_key)
# print("Asymmetric decrypt symmetric key:", asymmetric_decrypted_symmetric_key)
