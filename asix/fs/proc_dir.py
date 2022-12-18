from .dir import FSDir
from .perm import FSPerm
from .proc_info_dir import FSProcInfoDir
from .utils import SYSTEM


__all__ = ["FSProcDir"]


class FSProcDir(FSDir):
    def __init__(self, proc: int) -> None:
        super().__init__()
        self.proc = proc
        self.set_perm(proc, FSPerm.RX)
        self.set_entry("self", FSProcInfoDir(proc), SYSTEM)

        tmp_dir = FSDir()
        tmp_dir.set_perm(proc, FSPerm.RWX)
        self.set_entry("tmp", tmp_dir, SYSTEM)
