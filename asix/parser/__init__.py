from typing import Callable
from .utils import *
from .branch import *
from .function import *
from .lines import *
from .part_1 import lex_lines
from .part_2 import get_function_registry
from .part_3 import resolve_imports
from .part_4 import inline_functions
from .part_5 import process_branches


def parse(content: str, load: Callable[[str], str]):
    lines = lex_lines(content.splitlines())
    reg = get_function_registry(lines, is_library=False)

    def get_sub_reg(path: str):
        content = load(path)
        lines = lex_lines(content.splitlines())
        return get_function_registry(lines, is_library=True)

    resolve_imports(reg, get_sub_reg)

    inlined = inline_functions(reg)
    return process_branches(inlined)
