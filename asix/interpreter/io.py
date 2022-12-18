from typing import TYPE_CHECKING


from .utils import get_fs_path
from ..parser import (
    DataLine,
)

if TYPE_CHECKING:
    from ..fs import FS


def execute_io(line: DataLine, fs: "FS", proc: int) -> None:
    fs.write_file(
        get_fs_path(line.destination.text),
        fs.read_file(get_fs_path(line.source.text), proc),
        proc,
    )
