from .stdio import FSStdErr, FSStdIn, FSStdOut
from .dir import FSDir
from .file import FSFile
from .perm import FSPerm
from .raw import FSRaw
from .utils import SYSTEM


__all__ = ["FSProcInfoDir"]


class FSProcInfoDir(FSDir):
    def __init__(self, proc: int) -> None:
        super().__init__()
        self.set_perm(proc, FSPerm.RX)
        self.set_entry("id", FSRaw(str(proc)), SYSTEM)

        stdin = FSStdIn()
        stdin.set_perm(proc, FSPerm.RW)
        self.set_entry("stdin", stdin, SYSTEM)

        stdout = FSStdOut()
        stdout.set_perm(proc, FSPerm.RW)
        self.set_entry("stdout", stdout, SYSTEM)

        stderr = FSStdErr()
        stderr.set_perm(proc, FSPerm.RW)
        self.set_entry("stderr", stderr, SYSTEM)

        status = FSFile("0")
        status.set_perm(proc, FSPerm.RW)
        self.set_entry("status", status, SYSTEM)
