from typing import TYPE_CHECKING, List, Set
from html import escape
from subprocess import Popen, DEVNULL
from datetime import datetime, timedelta
import atexit

if TYPE_CHECKING:
    from ..parser import Branch


HEADER = """digraph G {

node[shape=Mrecord, fontname="Fira Code", fontsize="8"]
edge[tailclip=false, headclip=false]
entry[shape=doublecircle, label=""]
"""

FOOTER = """
}
"""

subprocesses: List[Popen[bytes]] = []


def graph_branches(entry: "Branch", branches: Set["Branch"], filename: str) -> None:
    ids = {branch: id for id, branch in enumerate(branches)}

    with open(filename, "wt") as f:
        f.write(HEADER)

        for branch, id in ids.items():
            content = (
                "\\n".join(map(lambda i: escape(str(i)), branch.content)) or "[noop]"
            )
            condition = escape(str(branch.condition))
            branch_row = (
                ""
                if branch.true_branch == branch.false_branch
                else ("|{<f>|" + condition + "|<t>}")
            )

            f.write("_" + str(id) + '[label="{' + content + branch_row + '}"]\n')

            if branch.true_branch:
                if branch.true_branch == branch.false_branch:
                    f.write(
                        "_"
                        + str(id)
                        + ":s -> _"
                        + str(ids[branch.true_branch])
                        + ":n\n"
                    )
                    continue

                f.write(
                    "_"
                    + str(id)
                    + ":t:c -> _"
                    + str(ids[branch.true_branch])
                    + ':n [color="green"]\n'
                )

            if branch.false_branch:
                f.write(
                    "_"
                    + str(id)
                    + ":f:c -> _"
                    + str(ids[branch.false_branch])
                    + ':n [color="red"]\n'
                )

        f.write("entry:c -> _" + str(ids[entry]) + ":n [tailclip=true]\n")
        f.write(FOOTER)

    subprocesses.append(
        Popen(
            [
                "dot",
                "-Tsvg",
                "-O",
                filename,
            ],
            stdin=DEVNULL,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
    )


SUBPROCESSES_TIMEOUT = timedelta(seconds=5)


def cleanup_subprocesses() -> None:
    begin = datetime.now() + SUBPROCESSES_TIMEOUT

    for s in subprocesses:
        if s.poll() != None:
            continue

        timeout = (begin - datetime.now()).total_seconds()
        if timeout > 0:
            s.wait(timeout)
        else:
            s.kill()


atexit.register(cleanup_subprocesses)
