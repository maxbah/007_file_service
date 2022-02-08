#! /usr/bin/env python3
import argparse
import os

from src import file_service


def read_file():
    """
    Function to read filename
    :return: None
    """
    filename = input('Enter file name: ')
    if os.path.exists(filename):
        content = file_service.read_file(filename)
        print(f'Reading - {filename}. File content: {content}')
    else:
        print('File not exist')


def create_file():
    """
    Function to create file
    :return: None
    """
    content = input('Please type file content: ')
    file_service.create_file(content)


def delete_file():
    """
    Function to delete file
    :return: None
    """
    filename = input('Enter file name to del: ')
    if os.path.isfile(filename):
        file_service.delete_file(filename)
        print(f'File - {filename} deleted.')
    else:
        print('File doesnt exist.')


def list_dir():
    """
    Function to get list dirs
    :return: None
    """
    f_path = input('Enter path to listdir: ')
    l_dirs = file_service.list_dir(f_path)
    print(f'{f_path} list dirs: {l_dirs}')


def change_dir():
    """
    Function to change directory
    :return: None
    """
    directory = input('Enter directory: ')
    if os.path.isdir(directory):
        file_service.change_dir(directory)
        cur_dir = file_service.get_cwd()
        print(f'Directory changed to {cur_dir}')
    else:
        print('Directory doesnt exist')


def get_file_permissions():
    """
    Function to get file permission
    :return: None
    """
    filename = input("Enter file name : ")
    if os.path.exists(filename):
        permissions = os.stat(filename).st_mode
        print(f"file permissions : {permissions}")
    else:
        print('File not existed')


def set_file_permissions():
    """
    Function to set file permission
    :return: None
    """
    filename = input("Enter file name : ")
    if os.path.exists(filename):
        permissions = input("Input UNIX permissions in oct format (777):")
        print(f"Set {permissions} to {filename}")
        os.chmod(filename, int(permissions))
    else:
        print('File not existed')


def get_cwd():
    """
    Function to get current directory
    :return: None
    """
    wd = os.getcwd()
    print(f" Currently we in: {wd}")


def get_metadata():
    """
    Function to get metadata
    :return: tuple
    """
    filename = input("Enter file name : ")
    metadata = file_service.file_service.get_file_metadata(filename)
    print(f"Metadata for {filename}: {metadata}")


def main():
    """
    Main function
    :return: None
    """
    # Create argument parser that will retrieve working directory
    parser = argparse.ArgumentParser(description='Restfull file server.')
    parser.add_argument('-d', '--directory', dest='path', help='Path to working directory')
    args = parser.parse_args()
    commands = {
        "get": read_file,
        "create": create_file,
        "delete": delete_file,
        "ls": list_dir,
        "cd": change_dir,
        "get_perm": get_file_permissions,
        "set_perm": set_file_permissions,
        "cwd": get_cwd,
        "mtd": get_metadata
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


if __name__ == "__main__":
    main()
