from ..fs import FSPath, get_path


RUN_PATH = FSPath("/run/")
SELF_STATUS_PATH = FSPath("/run/self/status")


def get_fs_path(path: str) -> FSPath:
    return get_path(path).to_absolute(RUN_PATH)
