from typing import (
    Iterable,
    Optional,
    Set,
)

from .function import *
from .lines import (
    CommandLine,
    EndFunctionLine,
    FunctionCallLine,
    FunctionLine,
    ImportLine,
    AnyLine,
)


def get_function_registry(
    lines: Iterable[AnyLine], is_library: bool
) -> FunctionRegistry:
    reg = FunctionRegistry()
    current: Optional[Function] = None
    fc_lines: Set[FunctionCallLine] = set()

    for line in lines:
        if isinstance(line, FunctionLine):
            assert not current, f"“{current.fn}” is not finished for “{line}” to start"
            current = Function(line)
            reg.add_function(current)
        elif isinstance(line, EndFunctionLine):
            assert current, f"Lone “{line}”"
            current.nf = line
            current = None
        elif isinstance(line, ImportLine):
            assert not current, f"“{line}” cannot be nested inside “{current.fn}”"
            reg.add_import(line)
        elif (
            is_library
            and isinstance(line, CommandLine)
            and line.command.text == "not_execute"
        ):
            pass
        elif current:
            current.add_line(line)
        else:
            reg.add_line(line)

        if isinstance(line, FunctionCallLine):
            fc_lines.add(line)

    assert not current, f"“{current.fn}” is unbalanced"

    for line in fc_lines:
        line.target = reg.functions.get(line.name.text)

    return reg
