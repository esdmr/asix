from re import Pattern, compile

from .utils import Range, Substring
from .lines import *
from typing import (
    Any,
    Generator,
    Iterable,
    List,
    Tuple,
)

MATCHERS: List[Tuple[Any, "Pattern[str]"]] = [
    (CommentLine, compile(r"^\s*(//)\s*(.*\S|)\s*$")),
    (DataLine, compile(r"^\s*(io)\s+(\S+)\s+(\S+)\s*$")),
    (CommandLine, compile(r"^\s*(do)\s+(\w+)\s*$")),
    (IfLine, compile(r"^\s*(if)\s+(\S+)\s*$")),
    (EndIfLine, compile(r"^\s*(fi)\s*$")),
    (LoopLine, compile(r"^\s*(br)\s*$")),
    (ImportLine, compile(r"^\s*(in)\s+(\S+)\s+(\w+)\s*$")),
    (FunctionCallLine, compile(r"^\s*(fc)\s+(\w+)\s*$")),
    (FunctionLine, compile(r"^\s*(fn)\s+(\w+)\s*$")),
    (EndFunctionLine, compile(r"^\s*(nf)\s*$")),
]

EMPTY_LINE = compile(r"^\s*$")


def lex_lines(lines: Iterable[str]) -> Generator[AnyLine, None, None]:
    comments: List[CommentLine] = []

    for row, line in enumerate(lines):
        if EMPTY_LINE.match(line):
            continue

        for cls, re in MATCHERS:
            if match := re.match(line):
                line = cls(
                    *[
                        Substring.from_match(row, match, i + 1)
                        for i, _ in enumerate(match.groups())
                    ],
                    Range.from_span(row, match.span()),
                )

                if isinstance(line, CommentLine):
                    comments.append(line)
                else:
                    line.comments = comments
                    comments = []
                    yield line

                break
        else:
            raise SyntaxError(f"Cannot parse line {row}: {line.strip()}")

    yield EOF(comments)
