import ast
from typing import Any, List, Optional, Set, Union
from json import dumps

import esprima.nodes as esn  # type: ignore

__all__ = ["Result", "get_super_class", "get_import_source"]


class Result:
    sfx_inject: Set[str]

    def __init__(
        self, node: Union[List[esn.Node], esn.Node, None] = None, *sfx_sources: "Result"
    ) -> None:
        self.node = node or [] if isinstance(node, list) or node == None else [node]
        self.sfx_inject = set()

        for other in sfx_sources:
            for i in other.sfx_inject:
                self.sfx_inject.add(i)

    def get(self):
        return self.node[0]

    def maybe_get(self):
        return self.node[0] if len(self.node) > 0 else None

    def set(self, value: esn.Node):
        self.node.clear()
        self.node.append(value)

    @staticmethod
    def _collect(*results: "Result"):
        for result in results:
            yield from result.node

    @staticmethod
    def collect(*results: "Result"):
        return [*Result._collect(*results)]

def get_super_class(stmt: ast.ClassDef) -> Result:
    if len(stmt.bases) > 1:
        raise NotImplementedError("Multiple inheritance is not implemented")

    result = Result()

    if len(stmt.bases) == 1:
        base = stmt.bases[0]

        if not isinstance(base, ast.Name):
            raise TypeError("Unhandled class base type: " + type(base).__name__)

        result.set(
            esn.CallExpression(
                esn.Identifier("__get_ctor__"), [esn.Identifier(base.id)]
            )
        )

        result.sfx_inject.add('__get_ctor__')

        if base.id == "Exception":
            result.sfx_inject.add(base.id)

    return result


def create_literal(text: Any) -> esn.Literal:
    return esn.Literal(text, dumps(text))


supported_modules = ['re', 'dataclasses', 'typing']


def get_import_source(filename: str, module: Optional[str], level: int = 0) -> Result:
    if level == 0:
        if module in supported_modules:
            return Result(create_literal(f"#python/{module}"))
        else:
            raise ValueError(f"Unsupported module: {module}")

    rel = "./" if level == 1 else "../" * (level - 1)

    # FIXME: We are hoping that it is a .js and not a /__init__.js here.
    path = rel + (module or "__init__").replace(".", "/") + ".mjs"
    return Result(create_literal(path))
