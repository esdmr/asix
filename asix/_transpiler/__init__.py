import ast
from typing import List

import esprima as es  # type: ignore
import esprima.nodes as esn  # type: ignore


from .utils import *


def from_file(filename: str) -> ast.Module:
    with open(filename, "rt") as f:
        content = f.read()

    return ast.parse(content, filename, "exec")


all_globals = (
    "__make_ctor__",
    "__get_ctor__",
    "isinstance",
    "Exception",
    "AssertionError",
    "__assert__",
    "None",
)


def process_module(module: ast.Module, filename: str) -> Result:
    list = [process_statement(stmt, filename) for stmt in module.body]

    body = Result.collect(*list)
    result = Result(esn.Module(body), *list)
    global_imports: List[str] = []

    for item in result.sfx_inject:
        if item in all_globals:
            global_imports.append(item)
        else:
            raise ValueError("Unknown injection: " + item)

    if len(global_imports) > 0:
        decl: esn.ImportDeclaration = es.parseModule("import{" + ",".join(global_imports) + "}from'#python/_global';").body[0]  # type: ignore
        body.insert(0, decl)

    result.sfx_inject.clear()
    return result


def process_statement(stmt: "ast.stmt", filename: str) -> Result:
    if isinstance(stmt, ast.ImportFrom):
        source = get_import_source(filename, stmt.module, stmt.level)

        nodes: List[esn.Node] = [
            esn.ImportDeclaration(
                [
                    esn.ImportSpecifier(
                        esn.Identifier(i.asname or i.name), esn.Identifier(i.name)
                    )
                    for i in stmt.names
                ],
                esn.Literal(source, repr(source)),
            )
        ]  # type: ignore

        return Result(nodes)

    if isinstance(stmt, ast.ClassDef):
        superClass = get_super_class(stmt)
        body = [process_class_statement(i, filename) for i in stmt.body]

        nodes: List[esn.Node] = [
            esn.ExportNamedDeclaration(
                esn.ClassDeclaration(
                    esn.Identifier(stmt.name),
                    superClass.maybe_get(),
                    esn.ClassBody(Result.collect(*body)),
                ),
                [],
                None,
            ),
            es.parseModule(f"{stmt.name} = __make_ctor__({stmt.name});").body[0],  # type: ignore
        ]

        result = Result(nodes, superClass, *body)
        result.sfx_inject.add("__make_ctor__")

        return result

    if isinstance(stmt, ast.Pass):
        return Result()

    raise TypeError("Unhandled statement type: " + type(stmt).__name__)


def process_class_statement(stmt: "ast.stmt", filename: str) -> Result:
    if isinstance(stmt, ast.Pass):
        return Result()

    raise TypeError("Unhandled class body type: " + type(stmt).__name__)
