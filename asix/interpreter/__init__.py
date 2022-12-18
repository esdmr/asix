from typing import TYPE_CHECKING, Optional
from os.path import join
from .do import execute_do, reset_all
from .io import execute_io

from .graphviz import graph_branches

from ..errors import InterpreterInterrupt, StopInterpretation
from .utils import get_fs_path, SELF_STATUS_PATH
from ..parser import (
    DataLine,
    Substring,
    parse,
    Branch,
)

if TYPE_CHECKING:
    from ..fs import FS


def check_branch_condition(branch: Branch, fs: "FS", proc: int) -> bool:
    content = fs.read_file(
        get_fs_path(
            branch.condition.text
            if isinstance(branch.condition, Substring)
            else branch.condition
        ),
        proc,
    )

    return bool(content)


def execute_branch(branch: Branch, fs: "FS", proc: int) -> Optional[Branch]:
    for line in branch.content:
        try:
            if isinstance(line, DataLine):
                execute_io(line, fs, proc)
            else:
                execute_do(line, fs, proc)
        except InterpreterInterrupt:
            raise
        except Exception as e:
            raise RuntimeError(f"Error while executing “{line}”") from e

    return (
        branch.true_branch
        if branch.true_branch == branch.false_branch
        or check_branch_condition(branch, fs, proc)
        else branch.false_branch
    )


def interpret(content: str, fs: "FS", proc: int) -> int:
    def load(path: str) -> str:
        return fs.load_library(get_fs_path(path), proc)

    reset_all(fs.proc_dirs[proc])
    entry, branches = parse(content, load)

    if fs.branches_graph_dir:
        graph_branches(entry, branches, join(fs.branches_graph_dir, f"{proc}.dot"))

    current_branch: Optional[Branch] = entry

    try:
        while current_branch:
            current_branch = execute_branch(current_branch, fs, proc)
    except StopInterpretation:
        pass

    return int(fs.read_file(SELF_STATUS_PATH, proc) or "0")
