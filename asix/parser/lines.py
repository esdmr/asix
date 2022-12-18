from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
)

if TYPE_CHECKING:
    from .function import Function
    from .utils import Range, Substring

__all__ = [
    "CommentLine",
    "DataLine",
    "CommandLine",
    "IfLine",
    "EndIfLine",
    "LoopLine",
    "FunctionCallLine",
    "ImportLine",
    "FunctionLine",
    "EndFunctionLine",
    "AnyDataLine",
    "AnyInlineLine",
    "AnyContentLine",
    "AnyLine",
    "EOF",
]

@dataclass
class CommentLine:
    prefix: "Substring"
    content: "Substring"
    range: "Range"

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.prefix.text} {repr(self.content.text)}"


@dataclass
class DataLine:
    keyword: "Substring"
    source: "Substring"
    destination: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {repr(self.source.text)} {repr(self.destination.text)}"


@dataclass
class CommandLine:
    keyword: "Substring"
    command: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {self.command.text}"


@dataclass
class IfLine:
    keyword: "Substring"
    condition: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {repr(self.condition.text)}"


@dataclass
class EndIfLine:
    keyword: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text}"


@dataclass
class LoopLine:
    keyword: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text}"


@dataclass(eq=False)
class FunctionCallLine:
    keyword: "Substring"
    name: "Substring"
    range: "Range"
    target: Optional["Function"] = None
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {self.name.text}"


@dataclass(eq=False)
class ImportLine:
    keyword: "Substring"
    path: "Substring"
    namespace: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {repr(self.path.text)} {self.namespace.text}"


@dataclass
class FunctionLine:
    keyword: "Substring"
    name: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text} {self.name.text}"


@dataclass
class EndFunctionLine:
    keyword: "Substring"
    range: "Range"
    comments: List[CommentLine] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.range.start.row + 1}:] {self.keyword.text}"


@dataclass
class EOF:
    comments: List[CommentLine] = field(default_factory=list)


AnyDataLine = Union[DataLine, CommandLine]
AnyInlineLine = Union[AnyDataLine, IfLine, EndIfLine, LoopLine, EOF]
AnyContentLine = Union[AnyInlineLine, FunctionCallLine]
AnyLine = Union[AnyContentLine, ImportLine, FunctionLine, EndFunctionLine]
