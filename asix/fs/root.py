__all__ = ["FS"]

from typing import Callable, Dict, Optional

from .dev_dir import FSDevDir
from ..errors import InterpreterInterrupt
from .char_dir import FSCharDir
from .dir import FSDir
from .file import FSFile
from .path import FSPath
from .perm import FSPerm
from .proc_dir import FSProcDir
from .raw import FSRaw
from .str_dir import FSStrDir
from .symlink import FSSymlink
from .utils import GUEST, ROOT, SYSTEM, FSEntry


class FS(FSDir):
    proc_dirs: Dict[int, FSProcDir]
    branches_graph_dir = ""

    def __init__(self, execute: Callable[[str, "FS", int], int]) -> None:
        super().__init__()
        self.execute = execute
        self.proc_dirs = {}
        self.set_perm(GUEST, FSPerm.RX)
        self.set_entry("0", FSRaw(""), SYSTEM)
        self.set_entry("1", FSRaw("1"), SYSTEM)
        self.set_entry("str", FSStrDir(), SYSTEM)
        self.set_entry("char", FSCharDir(), SYSTEM)
        self.set_entry("dev", FSDevDir(), SYSTEM)

        for name in ["bin", "sbin", "lib", "slib"]:
            exec_dir = FSDir()
            exec_dir.set_perm(GUEST, FSPerm.RX)
            self.set_entry(name, exec_dir, SYSTEM)

        self.proc = FSDir()
        self.proc.set_perm(GUEST, FSPerm.R)
        self.set_entry("proc", self.proc, SYSTEM)

        tmp_dir = FSDir()
        tmp_dir.set_perm(GUEST, FSPerm.RWX)
        self.set_entry("tmp", tmp_dir, SYSTEM)

    def get_entry(self, name: str, proc: int) -> Optional[FSEntry]:
        if name == "run":
            symlink = FSSymlink(FSPath(f"/proc/{proc}/"))
            symlink.set_perm(proc, FSPerm.RW)
            return symlink

        return super().get_entry(name, proc)

    def change_perm(
        self,
        path: FSPath,
        other_proc: int,
        perm: FSPerm,
        self_proc: int,
        follow_symlinks: bool = True,
    ) -> None:
        assert (
            self_proc <= ROOT
        ), f"Currently, only ROOT or SYSTEM processes can change permissions (not {self_proc})"

        entry = path.get_result(self, self_proc).entry

        try:
            if isinstance(entry, FSFile) or isinstance(entry, FSDir):
                entry.set_perm(other_proc, perm)
            elif isinstance(entry, FSSymlink):
                if follow_symlinks:
                    self.change_perm(
                        entry.get_target(self_proc).to_absolute(path.get_dirname()),
                        other_proc,
                        perm,
                        self_proc,
                        follow_symlinks,
                    )
                else:
                    entry.set_perm(other_proc, perm)
            elif entry == None:
                raise FileNotFoundError("Entry not found")
            else:
                raise TypeError("Permission of entry cannot be changed")
        except Exception as e:
            raise RuntimeError(
                f"Error while changing the permission of “{path}”"
            ) from e

    def read_file(self, path: FSPath, proc: int) -> str:
        entry = path.get_result(self, proc).entry

        try:
            if isinstance(entry, FSFile):
                return entry.get_content(proc)
            elif isinstance(entry, FSSymlink):
                return self.read_file(
                    entry.get_target(proc).to_absolute(path.get_dirname()), proc
                )
            elif isinstance(entry, FSRaw):
                return entry.content
            elif entry == None:
                raise FileNotFoundError("Entry not found")
            else:
                raise TypeError(f"Not a readable entry")
        except Exception as e:
            raise RuntimeError(f"Error while reading from “{path}”") from e

    def write_file(self, path: FSPath, new_content: str, proc: int) -> None:
        result = path.get_result(self, proc)
        entry = result.entry

        try:
            if isinstance(entry, FSFile):
                entry.set_content(new_content, proc)
            elif isinstance(entry, FSSymlink):
                self.write_file(
                    entry.get_target(proc).to_absolute(path.get_dirname()),
                    new_content,
                    proc,
                )
            elif entry == None:
                entry = FSFile(new_content)
                entry.set_perm(proc, FSPerm.RW)
                result.entry = entry
            else:
                raise TypeError(f"Not a writable entry")
        except Exception as e:
            raise RuntimeError(f"Error while writing to “{path}”") from e

    def append_file(self, path: FSPath, new_content: str, proc: int) -> None:
        result = path.get_result(self, proc)
        entry = result.entry

        try:
            if isinstance(entry, FSFile):
                entry.append_content(new_content, proc)
            elif isinstance(entry, FSSymlink):
                self.append_file(
                    entry.get_target(proc).to_absolute(path.get_dirname()),
                    new_content,
                    proc,
                )
            elif entry == None:
                entry = FSFile(new_content)
                entry.set_perm(proc, FSPerm.RW)
                result.entry = entry
            else:
                raise TypeError(f"Not a appendable entry")
        except Exception as e:
            raise RuntimeError(f"Error while appending to “{path}”") from e

    def execute_file(self, path: FSPath, proc: int) -> int:
        entry = path.get_result(self, proc).entry

        try:
            if isinstance(entry, FSFile):
                return entry.execute_content(self, proc)
            elif isinstance(entry, FSSymlink):
                return self.execute_file(
                    entry.get_target(proc).to_absolute(path.get_dirname()), proc
                )
            elif entry == None:
                raise FileNotFoundError("Entry not found")
            else:
                raise TypeError(f"Not a executable entry")
        except InterpreterInterrupt:
            raise
        except Exception as e:
            raise RuntimeError(f"Error while executing “{path}”") from e

    def load_library(self, path: FSPath, proc: int) -> str:
        entry = path.get_result(self, proc).entry

        try:
            if isinstance(entry, FSFile):
                return entry.load_content(self, proc)
            elif isinstance(entry, FSSymlink):
                return self.load_library(
                    entry.get_target(proc).to_absolute(path.get_dirname()), proc
                )
            elif entry == None:
                raise FileNotFoundError("Entry not found")
            else:
                raise TypeError(f"Not a importable entry")
        except InterpreterInterrupt:
            raise
        except Exception as e:
            raise RuntimeError(f"Error while importing “{path}”") from e
