from typing import TYPE_CHECKING, List

from .lines import FunctionCallLine, AnyContentLine, AnyInlineLine

if TYPE_CHECKING:
    from .function import Function, FunctionRegistry


def inline_functions(reg: "FunctionRegistry") -> List[AnyInlineLine]:
    def inline(
        lines: List[AnyContentLine],
        inlined: List[AnyInlineLine],
        *stack: "Function",
    ):
        for line in lines:
            if isinstance(line, FunctionCallLine):
                name = line.name.text
                target = line.target or reg.functions[name]

                assert not (
                    target in stack
                ), f"Function cycle found: {', '.join(map(lambda f: f.name, stack))}, {name}"
                inline(target.content, inlined, *stack, target)
            else:
                inlined.append(line)

    assert len(reg.imports) == 0, "Cannot inline functions with unresolved imports"
    inlined: List[AnyInlineLine] = []
    inline(reg.global_content, inlined)
    return inlined
