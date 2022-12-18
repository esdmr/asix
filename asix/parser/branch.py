from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Set,
    Union,
)

if TYPE_CHECKING:
    from .lines import AnyDataLine
    from .utils import Substring

__all__ = ["TRUE_BRANCH", "FALSE_BRANCH", "Branch"]

TRUE_BRANCH = "/1"
FALSE_BRANCH = "/0"


class Branch:
    content: List["AnyDataLine"]
    parents: Set["Branch"]
    condition: Union["Substring", str]
    true_branch: Optional["Branch"]
    false_branch: Optional["Branch"]

    def __init__(self) -> None:
        self.content = []
        self.parents = set()
        self.condition = TRUE_BRANCH
        self.true_branch = None
        self.false_branch = None

    def set_branch(
        self, branch: Optional["Branch"], which: Optional[bool] = None
    ) -> None:
        if which != False:
            if self.true_branch:
                self.true_branch.parents.remove(self)
            self.true_branch = branch

        if which != True:
            if self.false_branch:
                self.false_branch.parents.remove(self)
            self.false_branch = branch

        if self.true_branch:
            self.true_branch.parents.add(self)
        if self.false_branch:
            self.false_branch.parents.add(self)

    def __str__(self) -> str:
        repr = object.__repr__
        parents = ", ".join(map(repr, self.parents)) or "<empty list>"
        content = "\n".join(map(str, self.content)) or "<empty list>"

        target = (
            f"  goto: {repr(self.true_branch)}"
            if self.true_branch == self.false_branch
            else f"""  if: {self.condition}
  then: {repr(self.true_branch)}
  else: {repr(self.false_branch)}"""
        )

        return f"""{repr(self)}: from {parents}
{content}
{target}"""
