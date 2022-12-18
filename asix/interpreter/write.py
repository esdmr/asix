from .utils import get_fs_path
from ..fs import SYSTEM, FSDir, FSFile, FSPath, FSPerm, FS, FSProcDir

WRITE_APPEND_PATH = FSPath("/run/write/append")
WRITE_LEN_PATH = FSPath("/run/write/len")
WRITE_DST_PATH = FSPath("/run/write/dst")


def reset_write(proc_dir: FSProcDir) -> None:
    write_dir = FSDir()
    write_dir.set_perm(proc_dir.proc, FSPerm.RWX)
    proc_dir.set_entry("write", write_dir, SYSTEM)

    for name, content in [("len", "0"), ("dst", ""), ("append", "")]:
        write_file = FSFile(content)
        write_file.set_perm(proc_dir.proc, FSPerm.RW)
        write_dir.set_entry(name, write_file, SYSTEM)


def do_write(fs: FS, proc: int) -> None:
    length = int(fs.read_file(WRITE_LEN_PATH, proc))
    assert length > 0, "Nothing to write"

    dst = get_fs_path(fs.read_file(WRITE_DST_PATH, proc))
    append = bool(fs.read_file(WRITE_APPEND_PATH, proc))

    args = (
        dst,
        "".join([fs.read_file(FSPath(f"/run/write/{i}"), proc) for i in range(length)]),
        proc,
    )

    if append:
        fs.append_file(*args)
    else:
        fs.write_file(*args)
