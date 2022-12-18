from typing import Callable
from .file import FSFile
from .perm import FSPerm
from .utils import SYSTEM


__all__ = ["FSReadableStream"]


class FSReadableStream(FSFile):
    def __init__(self, fetch_line: Callable[[], str]) -> None:
        super().__init__()
        self.__fetch_line = fetch_line

    def get_content(self, proc: int) -> str:
        content = super().get_content(proc)
        super().set_content("", SYSTEM)
        return content

    def get_perm(self, proc: int) -> FSPerm:
        if proc == SYSTEM:
            return FSPerm.RWX

        return super().get_perm(proc) & FSPerm.R

    def fetch_line(self) -> bool:
        content = self.__fetch_line()
        self.append_content(content.rstrip("\n"), SYSTEM)
        return content == ""
