from typing import (
    TYPE_CHECKING,
    Callable,
    List,
)

if TYPE_CHECKING:
    from .function import FunctionRegistry
    from .lines import AnyContentLine


def resolve_imports(
    reg: "FunctionRegistry", get_sub_reg: Callable[[str], "FunctionRegistry"]
) -> None:
    global_content: List["AnyContentLine"] = []

    for line in reg.imports:
        try:
            sub_reg = get_sub_reg(line.path.text)
        except Exception as e:
            raise RuntimeError(f"Error while resolving “{line}”") from e

        assert (
            len(sub_reg.imports) == 0
        ), f"Library “{line.path}” still has some imports (All libraries should be flattened via “/sbin/ld”)"

        global_content += sub_reg.global_content

        for func in sub_reg.functions.values():
            func.name = line.namespace.text + "__" + func.name
            reg.add_function(func)

    global_content += reg.global_content
    reg.global_content = global_content
    reg.imports.clear()
