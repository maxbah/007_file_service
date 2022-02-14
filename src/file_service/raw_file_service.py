import file_service
from typing import Tuple


class RawFileService(file_service.FileService):
    def __init__(self, workdir):
        self.workdir = workdir

    def read(self, filename : str) -> str:
        return ""

    def write(self, data : str) -> str:
        return ""

    def ls(self) -> [str]:
        return []

    def cd(self, dir : str) -> None:
        # do not modify system work dir
        pass

    def remove(self, filename: str) -> None:
        pass

    def read_metadata(self, filename : str) -> Tuple[int, int, int]:
        return (0,0,0)
