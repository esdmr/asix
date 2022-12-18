import sys

from .readable_stream import FSReadableStream
from .writable_stream import FSWritableStream


__all__ = ["FSStdIn", "FSStdOut", "FSStdErr", "FSNullStream"]


class FSStdIn(FSReadableStream):
    def __init__(self) -> None:

        super().__init__(lambda: sys.stdin.readline())


class FSStdOut(FSWritableStream):
    def __init__(self) -> None:
        super().__init__(lambda s: print(s, end="", flush=True))


class FSStdErr(FSWritableStream):
    def __init__(self) -> None:
        super().__init__(lambda s: print(s, file=sys.stderr, end="", flush=True))


class FSNullStream(FSWritableStream):
    def __init__(self) -> None:
        super().__init__(lambda s: None)
