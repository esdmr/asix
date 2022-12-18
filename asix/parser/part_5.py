from typing import List, Set, Tuple

from .branch import Branch
from .lines import EOF, EndIfLine, IfLine, LoopLine, AnyInlineLine


def process_branches(inlined: List[AnyInlineLine]) -> Tuple[Branch, Set[Branch]]:
    entry = Branch()
    branches: Set[Branch] = set([entry])
    levels = [entry]
    skipped_levels = 0

    for line in inlined:
        if skipped_levels > 0:
            if isinstance(line, IfLine):
                skipped_levels += 1
            elif isinstance(line, EndIfLine):
                skipped_levels -= 1

                if skipped_levels == 0:
                    if_branch = levels.pop()
                    condition_branch = levels.pop()

                    after_branch = Branch()
                    branches.add(after_branch)
                    if_branch.set_branch(condition_branch)
                    condition_branch.set_branch(after_branch, False)

                    levels[-1] = after_branch
        elif isinstance(line, IfLine):
            condition_branch = Branch()
            branches.add(condition_branch)
            condition_branch.condition = line.condition
            levels[-1].set_branch(condition_branch)
            levels.append(condition_branch)

            if_branch = Branch()
            branches.add(if_branch)
            condition_branch.set_branch(if_branch, True)

            levels.append(if_branch)
        elif isinstance(line, EndIfLine):
            if_branch = levels.pop()
            condition_branch = levels.pop()

            before_branch = levels.pop()
            before_branch.condition = condition_branch.condition
            before_branch.set_branch(condition_branch.true_branch, True)
            branches.remove(condition_branch)

            after_branch = Branch()
            branches.add(after_branch)
            if_branch.set_branch(after_branch)
            before_branch.set_branch(after_branch, False)

            levels.append(after_branch)
        elif isinstance(line, LoopLine):
            skipped_levels += 1
        elif isinstance(line, EOF):
            pass
        else:
            levels[-1].content.append(line)

    assert skipped_levels == 0, "Lone br?"
    assert len(levels) == 1, "Lone if?"

    for branch in set(branches):
        if (
            len(branch.content) == 0
            and branch.true_branch == branch.false_branch == None
        ):
            for parent in set(branch.parents):
                if parent.true_branch == branch:
                    parent.set_branch(None, True)
                if parent.false_branch == branch:
                    parent.set_branch(None, False)

                try:
                    branches.remove(branch)
                except KeyError:
                    pass

    return entry, branches
