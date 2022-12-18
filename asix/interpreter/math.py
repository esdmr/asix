from typing import Callable, Dict
from ..fs import SYSTEM, FSDir, FSFile, FSPath, FSPerm, FS, FSProcDir


MATH_A_PATH = FSPath("/run/math/a")
MATH_F_PATH = FSPath("/run/math/f")
MATH_B_PATH = FSPath("/run/math/b")
MATH_OUT_PATH = FSPath("/run/math/out")

math_commands: Dict[str, Callable[[str, str], str]] = {
    "+": lambda a, b: str(float(a) + float(b)),
    "-": lambda a, b: str(float(a) - float(b)),
    "*": lambda a, b: str(float(a) * float(b)),
    "**": lambda a, b: str(float(a) ** float(b)),
    "/": lambda a, b: str(float(a) / float(b)),
    "%": lambda a, b: str(float(a) % float(b)),
    "==": lambda a, b: "1" if float(a) == float(b) else "",
    "!=": lambda a, b: "1" if float(a) != float(b) else "",
    "<=": lambda a, b: "1" if float(a) <= float(b) else "",
    ">=": lambda a, b: "1" if float(a) >= float(b) else "",
    "<": lambda a, b: "1" if float(a) < float(b) else "",
    ">": lambda a, b: "1" if float(a) > float(b) else "",
    "eq": lambda a, b: "1" if a == b else "",
    "ne": lambda a, b: "1" if a != b else "",
    "and": lambda a, b: "1" if a and b else "",
    "or": lambda a, b: "1" if a or b else "",
    "xor": lambda a, b: "1" if a != b else "",
    "nand": lambda a, b: "1" if not a or not b else "",
    "nor": lambda a, b: "1" if not a and not b else "",
    "xnor": lambda a, b: "1" if a == b else "",
}


def reset_math(proc_dir: FSProcDir) -> None:
    math_dir = FSDir()
    math_dir.set_perm(proc_dir.proc, FSPerm.RX)
    proc_dir.set_entry("math", math_dir, SYSTEM)

    for name in ["a", "f", "b", "out"]:
        math_file = FSFile()
        math_file.set_perm(proc_dir.proc, FSPerm.RW)
        math_dir.set_entry(name, math_file, SYSTEM)


def do_math(fs: FS, proc: int) -> None:
    fs.write_file(
        MATH_OUT_PATH,
        math_commands[fs.read_file(MATH_F_PATH, proc)](
            fs.read_file(MATH_A_PATH, proc), fs.read_file(MATH_B_PATH, proc)
        ),
        proc,
    )
