from typing import Any, Generator, Optional, TypeVar, Union, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from .dir import FSDir
    from .file import FSFile
    from .raw import FSRaw
    from .symlink import FSSymlink


__all__ = [
    "FSEntry",
    "SYSTEM",
    "ROOT",
    "GUEST",
    "get_new_proc_id",
    "T",
    "get_generator_value",
]


FSEntry = Union["FSDir", "FSFile", "FSSymlink", "FSRaw"]
SYSTEM = -3
ROOT = -2
GUEST = -1
proc_counter = 0


def get_new_proc_id() -> int:
    global proc_counter
    sub_proc = proc_counter
    proc_counter += 1
    return sub_proc


T = TypeVar("T")


def get_generator_value(gen: Generator[Any, None, T]) -> T:
    value: Optional[T] = None

    def iter() -> Generator[Any, None, None]:
        nonlocal value
        value = yield from gen

    for _ in iter():
        pass

    return cast(T, value)
