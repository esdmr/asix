from .perm import FSPerm


__all__ = ["FSRaw"]


class FSRaw:
    def __init__(self, content: str) -> None:
        self.content = content

    def get_perm(self, proc: int) -> FSPerm:
        return FSPerm.R
