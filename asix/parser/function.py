from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Set,
)

if TYPE_CHECKING:
    from .lines import (
        AnyContentLine,
        EndFunctionLine,
        FunctionLine,
        ImportLine,
    )

__all__ = ["Function", "FunctionRegistry"]


@dataclass(kw_only=True)
class Function:
    fn: "FunctionLine"
    nf: Optional["EndFunctionLine"]
    content: List["AnyContentLine"]
    name: str

    def __init__(self, fn: "FunctionLine") -> None:
        self.fn = fn
        self.nf = None
        self.content = []
        self.name = fn.name.text

    def add_line(self, line: "AnyContentLine") -> None:
        self.content.append(line)

    def __str__(self) -> str:
        content = "\n".join(map(str, self.content))
        return f"[{self.fn.range.start.row + 1}:] function {self.name}\n{content}\n{self.nf}"


@dataclass(kw_only=True)
class FunctionRegistry:
    functions: Dict[str, Function]
    global_content: List["AnyContentLine"]
    imports: Set["ImportLine"]

    def __init__(self) -> None:
        self.functions = {}
        self.global_content = []
        self.imports = set()

    def add_function(self, function: Function) -> None:
        self.functions[function.name] = function

    def add_line(self, line: "AnyContentLine") -> None:
        self.global_content.append(line)

    def add_import(self, line: "ImportLine") -> None:
        self.imports.add(line)

    def __str__(self) -> str:
        functions = "\n\n".join(map(str, self.functions.values()))
        content = "\n".join(map(str, self.global_content))
        return f"{functions}\n\n{content}"
