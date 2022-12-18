from typing import TYPE_CHECKING
from .entry_info import FSEntryInfo
from .perm import FSPerm

if TYPE_CHECKING:
    from .path import FSAnyPath


__all__ = ["FSSymlink"]


class FSSymlink(FSEntryInfo):
    def __init__(self, target: "FSAnyPath") -> None:
        super().__init__()
        self.__target = target

    def get_target(self, proc: int) -> "FSAnyPath":
        assert (
            self.get_perm(proc) & FSPerm.R
        ), f"Process {proc} is not allowed to resolve this symbolic link"

        return self.__target

    def set_target(self, new_content: "FSAnyPath", proc: int) -> None:
        assert (
            self.get_perm(proc) & FSPerm.W
        ), f"Process {proc} is not allowed to update this symbolic link"

        self.__target = new_content

    def get_perm(self, proc: int) -> FSPerm:
        return super().get_perm(proc) & ~FSPerm.X
