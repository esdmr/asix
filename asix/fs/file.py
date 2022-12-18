from typing import TYPE_CHECKING
from .entry_info import FSEntryInfo
from .perm import FSPerm

if TYPE_CHECKING:
    from .root import FS


__all__ = ["FSFile"]


class FSFile(FSEntryInfo):
    def __init__(self, content: str = "") -> None:
        super().__init__()
        self.__content = content

    def get_content(self, proc: int) -> str:
        assert (
            self.get_perm(proc) & FSPerm.R
        ), f"Process {proc} is not allowed to read from this file"

        return self.__content

    def set_content(self, new_content: str, proc: int) -> None:
        assert (
            self.get_perm(proc) & FSPerm.W
        ), f"Process {proc} is not allowed to write to this file"

        self.__content = new_content

    def append_content(self, new_content: str, proc: int) -> None:
        assert (
            self.get_perm(proc) & FSPerm.W
        ), f"Process {proc} is not allowed to append to this file"

        self.__content += new_content

    def execute_content(self, fs: "FS", proc: int) -> int:
        from .proc_dir import FSProcDir
        from .utils import SYSTEM, get_new_proc_id

        assert (
            self.get_perm(proc) & FSPerm.RX == FSPerm.RX
        ), f"Process {proc} is not allowed to execute this file"

        sub_proc = get_new_proc_id()

        proc_dir = FSProcDir(sub_proc)
        fs.proc.set_entry(str(sub_proc), proc_dir, SYSTEM)
        fs.proc_dirs[sub_proc] = proc_dir

        status = fs.execute(self.__content, fs, sub_proc)

        del fs.proc_dirs[sub_proc]
        fs.proc.set_entry(str(sub_proc), None, SYSTEM)

        return status

    def load_content(self, fs: "FS", proc: int) -> str:
        assert (
            self.get_perm(proc) & FSPerm.RX == FSPerm.RX
        ), f"Process {proc} is not allowed to import this file"

        return self.__content
