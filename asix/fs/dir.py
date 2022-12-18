from typing import Dict, Generator, Optional
from .entry_info import FSEntryInfo
from .perm import FSPerm
from .utils import FSEntry

__all__ = ["FSDir"]


class FSDir(FSEntryInfo):
    __entries: Dict[str, FSEntry]

    def __init__(self) -> None:
        super().__init__()
        self.__entries = {}

    def get_entry(self, name: str, proc: int) -> Optional[FSEntry]:
        assert (
            self.get_perm(proc) & FSPerm.R
        ), f"Process {proc} is not allowed to read from this directory"
        return self.__entries.get(name)

    def set_entry(self, name: str, entry: Optional[FSEntry], proc: int) -> None:
        assert (
            self.get_perm(proc) & FSPerm.W
        ), f"Process {proc} is not allowed to write to this directory"

        if entry:
            self.__entries[name] = entry
        else:
            del self.__entries[name]

    def entries(self, proc: int) -> Generator[str, None, None]:
        assert (
            self.get_perm(proc) & FSPerm.X
        ), f"Process {proc} is not allowed to search this directory"

        for key in self.__entries.keys():
            yield key
