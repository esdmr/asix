from .stdio import FSNullStream, FSStdErr, FSStdIn, FSStdOut
from .dir import FSDir
from .perm import FSPerm
from .utils import GUEST, SYSTEM


__all__ = ["FSDevDir"]


class FSDevDir(FSDir):
    def __init__(self) -> None:
        super().__init__()
        self.set_perm(GUEST, FSPerm.RX)

        self.set_entry("stdin", FSStdIn(), SYSTEM)
        self.set_entry("stdout", FSStdOut(), SYSTEM)
        self.set_entry("stderr", FSStdErr(), SYSTEM)

        null = FSNullStream()
        null.set_perm(GUEST, FSPerm.W)
        self.set_entry("null", null, SYSTEM)
