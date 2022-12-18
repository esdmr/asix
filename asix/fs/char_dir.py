from typing import Optional
from .dir import FSDir
from .perm import FSPerm
from .raw import FSRaw
from .utils import SYSTEM, FSEntry

__all__ = ["FSCharDir"]

CHAR_MAPPING = {
    "\\": "\\",
    "\\\\": "\\",
    "\\b": "\b",
    "\\f": "\f",
    "\\n": "\n",
    "\\r": "\r",
    "\\t": "\t",
    "null": "\0",
    "spc": " ",
    "nul": "\x00",
    "soh": "\x01",
    "stx": "\x02",
    "etx": "\x03",
    "eot": "\x04",
    "enq": "\x05",
    "ack": "\x06",
    "bel": "\x07",
    "bs": "\x08",
    "ht": "\x09",
    "lf": "\x0A",
    "vt": "\x0B",
    "ff": "\x0C",
    "cr": "\x0D",
    "so": "\x0E",
    "si": "\x0F",
    "dle": "\x10",
    "dc1": "\x11",
    "dc2": "\x12",
    "dc3": "\x13",
    "dc4": "\x14",
    "nak": "\x15",
    "syn": "\x16",
    "etb": "\x17",
    "can": "\x18",
    "em": "\x19",
    "sub": "\x1A",
    "esc": "\x1B",
    "fs": "\x1C",
    "gs": "\x1D",
    "rs": "\x1E",
    "us": "\x1F",
    "sp": "\x20",
    "del": "\x7F",
}


class FSCharDir(FSDir):
    def get_entry(self, name: str, proc: int) -> Optional[FSEntry]:
        name = name.lower()

        if name in CHAR_MAPPING:
            return FSRaw(CHAR_MAPPING[name])
        elif name.startswith("\\x") and len(name) == 4:
            return FSRaw(chr(int(name[2:], 16)))
        elif name.startswith("\\u") and len(name) == 6:
            return FSRaw(chr(int(name[2:], 16)))
        elif name.startswith("\\U") and len(name) == 10:
            return FSRaw(chr(int(name[2:], 16)))
        elif name.startswith("\\") and 2 <= len(name) <= 4:
            return FSRaw(chr(int(name[1:], 8)))

    def get_perm(self, proc: int) -> FSPerm:
        return FSPerm.RX if proc == SYSTEM else FSPerm.R
