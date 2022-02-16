#! /usr/bin/env python3
import argparse
import os
import logging
import logging.config
import yaml

from src.http_server import http_server, create_app
from aiohttp import web
from src.config import Config
from src.crypto.encription import SymmetricEncryption
from src.crypto.encription import AsymmetricEncryption
from src.file_service import RawFileService, SignedFileService, EncryptedFileService

symmetric = SymmetricEncryption()
asymmetric = AsymmetricEncryption()

file_services = RawFileService()
signed_file_service = SignedFileService(file_services)
encrypted_file_service = EncryptedFileService(file_services)


def read_file():
    """
    Function to read filename
    :return: None
    """
    filename = input('Enter file name: ')
    if os.path.exists(filename):
        content = file_services.read(filename)
        print(f'Reading - {filename}. File content: {content}')
    else:
        print('File not exist')


def reed_signed_file():
    """Function to reed file and signature
    :return: None
    """
    filename = input('Please type filename: ')
    data = file_services.read(filename)
    logging.info(f" Sign {filename} data: {data}")
    return data


def create():
    """
    Function to create file
    :return: None
    """
    content = input('Please type file content: ')
    file_services.create(content)


def create_signed_file():
    """Function to create file and signature
    :return: None
    """
    content = input('Please type file content: ')
    signer = input("Please type signature alg (md5 ao sha512)")
    signed_file_service.write(content, signer)


def create_encrypted_file():
    content = input("Enter file content: ")
    filename = encrypted_file_service.write(content)
    print(f"Creating encrypted file {filename} with content: \n{content}")


def delete_file():
    """
    Function to delete file
    :return: None
    """
    filename = input('Enter file name to del: ')
    if os.path.isfile(filename):
        file_services.remove(filename)
        print(f'File - {filename} deleted.')
    else:
        print('File doesnt exist.')


def list_dir():
    """
    Function to get list dirs
    :return: None
    """
    f_path = input('Enter path to listdir: ')
    l_dirs = file_services.ls(f_path)
    print(f'{f_path} list dirs: {l_dirs}')


def change_dir():
    """
    Function to change directory
    :return: None
    """
    dir = input('Enter directory: ')
    if os.path.isdir(dir):
        file_services.cd(dir)
        cur_dir = file_services.get_cwd()
        print(f'Directory changed to {cur_dir}')
    else:
        print('Directory doesnt exist')


def get_file_permissions():
    """
    Function to get file permission
    :return: None
    """
    filename = input("Enter file name : ")
    return file_services.get_file_permissions(filename)


def set_file_permissions():
    """
    Function to set file permission
    :return: None
    """
    filename = input("Enter file name : ")
    if os.path.exists(filename):
        permissions = int(input("Input UNIX permissions in oct format (777):"))
        file_services.set_file_permissions(filename, permissions)
    else:
        print('File not existed')


def get_cwd():
    """
    Function to get current directory
    :return: None
    """
    wd = file_services.get_cwd()
    print(f" Currently we in: {wd}")


def get_metadata():
    """
    Function to get metadata
    :return: tuple
    """
    filename = input("Enter file name : ")
    metadata = file_services.read_metadata(filename)
    print(f"Metadata for {filename}: {metadata}")


# Symmetric Encryption
def symm_encrypt():
    data = input("Please type data to symmetric encryption:")
    sym_enc_data = symmetric.encrypt(data)
    print("Symmetric encrypted data:", sym_enc_data)
    return sym_enc_data


def symm_decrypt():
    encrypted_data = input("Please type encrypted_data for symmetric decryption (str):")
    symmetric_decrypted_data = symmetric.decrypt(str.encode(encrypted_data), symmetric.f_key)
    return symmetric_decrypted_data


# Asymmetric Encryption
def storing_asymm_private_key_to_file():
    private_key_filename = input("Please type filename to store asymm private key (private_key):")
    print(f"Storing asymmetric private key to '{private_key_filename}.pem':", private_key_filename)
    return AsymmetricEncryption().storing_private_key_to_file(private_key_filename)


def storing_asymm_public_key_to_file():
    public_key_filename = input("Please type filename to store asymm public key (public_key):")
    print(f"Storing asymmetric public key to '{public_key_filename}.pem':", public_key_filename)
    return AsymmetricEncryption().storing_public_key_to_file(public_key_filename)


def reading_asymm_private_key():
    private_key_filename = input("Please type filename for reading asymm private key (private_key):")
    private_key = asymmetric.reading_private_key(private_key_filename)
    print(f"Reading private key from '{private_key_filename}.pem':", private_key)
    return private_key


def reading_asymm_public_key():
    public_key_filename = input("Please type filename for reading asymm public key (public_key):")
    public_key = asymmetric.reading_public_key(public_key_filename)
    print(f"Reading public key from '{public_key_filename}.pem':", public_key)
    return public_key


def asymm_encrypt():
    symmetric_key = input("Please type symmetric_key to asymmetric encryption:")
    asymmetric_encrypted_symmetric_key = asymmetric.encrypt(str.encode(symmetric_key))
    print("Asymmetric encrypt symmetric key:", asymmetric_encrypted_symmetric_key)
    return asymmetric_encrypted_symmetric_key


def asymm_decrypt():
    encrypted_symmetric_key = input("Please type encrypted_symmetric_key for asymmetric decryption:")
    asymmetric_decrypted_symmetric_key = asymmetric.decrypt(str.encode(encrypted_symmetric_key),
                                                            asymmetric.private_key)
    print("Asymmetric decrypt symmetric key:", asymmetric_decrypted_symmetric_key)
    return asymmetric_decrypted_symmetric_key


def console_main():
    """
    Main function
    :return: None
    """

    with open(file="./loger_config.yaml", mode='r') as file:
        logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
        logging.config.dictConfig(config=logging_yaml)

    logging.getLogger("telemetry").info("Start main.py execution")
    # Create argument parser that will retrieve working directory
    parser = argparse.ArgumentParser(description='Restfull file server.')
    parser.add_argument('-d', '--directory', dest='path', help='Path to working directory')
    args = parser.parse_args()

    default_config_name = 'src/config/config.ini'
    config = Config()
    config.load(default_config_name)
    logging.debug(f'Data from {default_config_name} loaded')

    commands = {
        "create": create,
        "reed": read_file,
        "reed_sig_f": reed_signed_file,
        "c_sig_f": create_signed_file,
        "c_enc_f": create_encrypted_file,
        "delete": delete_file,
        "ls": list_dir,
        "cd": change_dir,
        "get_perm": get_file_permissions,
        "set_perm": set_file_permissions,
        "cwd": get_cwd,
        "mtd": get_metadata,
        "get_algo": config.signature_algo,
        "sym_enc": symm_encrypt,
        "sym_dec": symm_decrypt,
        "private_key_to_f": storing_asymm_private_key_to_file,
        "public_key_to_f": storing_asymm_public_key_to_file,
        "private_key_read": reading_asymm_private_key,
        "public_key_read": reading_asymm_public_key,
        "asym_enc": asymm_encrypt,
        "asym_dec": asymm_decrypt,
    }
    while True:
        if args.path:
            os.chdir(args.path)
        command = input("Enter command: ")
        if command == "exit":
            return
        if command not in commands:
            print("Unknown command")
            continue
        command = commands[command]
        try:
            command()
        except Exception as ex:
            print(f"Error on {command} execution : {ex}")
    logging.getLogger("telemetry").info("End of main.py execution")


def main():
    app = create_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
