from typing import TYPE_CHECKING


from ..errors import StopInterpretation, StopProgram
from .math import do_math, reset_math
from .write import do_write, reset_write
from .fetch_line import do_fetch_line, reset_fetch_line

if TYPE_CHECKING:
    from ..fs import FS, FSProcDir
    from ..parser import (
        CommandLine,
    )


def reset_all(proc_dir: "FSProcDir") -> None:
    reset_math(proc_dir)
    reset_write(proc_dir)
    reset_fetch_line(proc_dir)


def execute_do(line: "CommandLine", fs: "FS", proc: int) -> None:
    command = line.command.text

    if command == "math":
        do_math(fs, proc)
    elif command == "reset_math":
        reset_math(fs.proc_dirs[proc])
    elif command == "write":
        do_write(fs, proc)
    elif command == "reset_write":
        reset_write(fs.proc_dirs[proc])
    elif command == "fetch_line":
        do_fetch_line(fs, proc)
    elif command == "reset_fetch_line":
        reset_fetch_line(fs.proc_dirs[proc])
    elif command == "reset_all":
        reset_all(fs.proc_dirs[proc])
    elif command == "not_execute":
        raise RuntimeError(f"This file is a library and should not be executed")
    elif command == "exit":
        raise StopInterpretation
    elif command == "halt":
        raise StopProgram
    else:
        raise ValueError(f"Unknown command “{line}”")
