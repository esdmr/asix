from typing import Callable
from .file import FSFile
from .perm import FSPerm
from .utils import SYSTEM


__all__ = ["FSWritableStream"]


class FSWritableStream(FSFile):
    corked = False

    def __init__(self, write: Callable[[str], None]) -> None:
        super().__init__()
        self.__write = write

    def set_content(self, new_content: str, proc: int) -> None:
        self.append_content(new_content, proc)

    def append_content(self, new_content: str, proc: int) -> None:
        super().append_content(new_content, proc)
        self.__flush()

    def get_perm(self, proc: int) -> FSPerm:
        if proc == SYSTEM:
            return FSPerm.RWX

        return super().get_perm(proc) & FSPerm.W

    def __flush(self) -> None:
        if not self.corked:
            self.__write(self.get_content(SYSTEM))
            super().set_content("", SYSTEM)
