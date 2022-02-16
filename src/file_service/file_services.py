from abc import ABCMeta, abstractmethod
from typing import Tuple


class FileService(metaclass=ABCMeta):

    @abstractmethod
    def read(self, filename: str) -> str: raise Exception("not implemented")

    @abstractmethod
    def write(self, data: str) -> str: raise Exception("not implemented")

    @abstractmethod
    def ls(self) -> [str]: raise Exception("not implemented")

    @abstractmethod
    def cd(self, dir: str) -> None: raise Exception("not implemented")

    @abstractmethod
    def remove(self, filename: str) -> None: raise Exception("not implemented")

    @abstractmethod
    def read_metadata(self, filename: str) -> Tuple[int, int, int]: raise Exception("not implemented")
