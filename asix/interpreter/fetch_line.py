from asix.fs.dir import FSDir
from .utils import get_fs_path
from ..fs import SYSTEM, FSFile, FSPath, FSPerm, FS, FSProcDir, FSReadableStream

FETCH_LINE_SRC_PATH = FSPath("/run/fetch_line/src")
FETCH_LINE_EOF_PATH = FSPath("/run/fetch_line/eof")
FETCH_LINE_DEFAULT = "/run/self/stdin"


def reset_fetch_line(proc_dir: FSProcDir) -> None:
    fetch_line_dir = FSDir()
    fetch_line_dir.set_perm(proc_dir.proc, FSPerm.RX)
    proc_dir.set_entry("fetch_line", fetch_line_dir, SYSTEM)

    src = FSFile(FETCH_LINE_DEFAULT)
    src.set_perm(proc_dir.proc, FSPerm.RW)
    fetch_line_dir.set_entry("src", src, SYSTEM)

    eof = FSFile()
    eof.set_perm(proc_dir.proc, FSPerm.RW)
    fetch_line_dir.set_entry("eof", eof, SYSTEM)


def do_fetch_line(fs: FS, proc: int) -> None:
    path = get_fs_path(fs.read_file(FETCH_LINE_SRC_PATH, proc))
    src = path.get_result(fs, proc).entry

    assert src, f"Cannot fetch line from the non-existent “{path}”"
    assert isinstance(
        src, FSReadableStream
    ), f"Cannot fetch line from the non-readable-stream “{path}”"

    fs.write_file(FETCH_LINE_EOF_PATH, "1" if src.fetch_line() else "", proc)
