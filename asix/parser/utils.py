from re import Match
from dataclasses import dataclass
from typing import (
    Tuple,
)

__all__ = ["Position", "Range", "Substring"]


@dataclass(order=True)
class Position:
    row: int
    col: int

    def __str__(self) -> str:
        return f"{self.row + 1}:{self.col + 1}"

    def __repr__(self) -> str:
        return f"Position({self.row}, {self.col})"


Span = Tuple[int, int]


@dataclass
class Range:
    start: Position
    end: Position

    @staticmethod
    def from_span(row: int, span: Span) -> "Range":
        return Range(Position(row, span[0]), Position(row, span[1]))

    def __str__(self) -> str:
        return f"{self.start} → {self.end}"

    def __repr__(self) -> str:
        return f"Range({repr(self.start)}, {repr(self.end)})"


@dataclass(kw_only=True)
class Substring:
    text: str
    range: Range

    @staticmethod
    def from_match(row: int, match: "Match[str]", group: int) -> "Substring":
        return Substring(
            text=match.group(group),
            range=Range.from_span(row, match.span(group)),
        )

    def __str__(self) -> str:
        return f"[{self.range.start}] {repr(self.text)}"
