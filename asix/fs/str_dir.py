from typing import Optional
from .dir import FSDir
from .perm import FSPerm
from .raw import FSRaw
from .utils import SYSTEM, FSEntry


__all__ = ["FSStrDir"]


class FSStrDir(FSDir):
    def get_entry(self, name: str, proc: int) -> Optional[FSEntry]:
        return FSRaw(name)

    def get_perm(self, proc: int) -> FSPerm:
        return FSPerm.RX if proc == SYSTEM else FSPerm.R
