from typing import Dict

from .perm import FSPerm
from .utils import GUEST, ROOT


__all__ = ["FSEntryInfo"]


class FSEntryInfo:
    __perms: Dict[int, FSPerm]

    def __init__(self) -> None:
        self.__perms = {}
        self.set_perm(GUEST, FSPerm.NONE)

    def get_perm(self, proc: int) -> FSPerm:
        if proc <= ROOT:
            return FSPerm.RWX

        return self.__perms[GUEST] | (self.__perms.get(proc) or FSPerm.NONE)

    def set_perm(self, proc: int, perm: FSPerm) -> None:
        self.__perms[proc] = perm
