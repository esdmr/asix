from typing import Any, Dict, List, Tuple, cast


INDENT = "  "


def _inspect_dict_item(key: object, value: object, level: int) -> str:
    return (
        INDENT * level
        + _inspect(key, level)
        + ": "
        + _inspect(value, level)
        + ",\n"
    )


def _inspect_list_item(value: object, level: int) -> str:
    return INDENT * level + _inspect(value, level) + ",\n"


def _inspect(obj: object, level: int) -> str:
    if any([isinstance(obj, c) for c in [str, int, float, bool, type(None)]]):
        return repr(obj)

    if isinstance(obj, dict):
        obj = cast(Dict[Any, Any], obj)
        name = type(obj).__name__

        if name != "dict":
            name += "(dict)"

        if len(obj) == 0:
            return name + " {}"

        return (
            name
            + " {\n"
            + "".join([_inspect_dict_item(k, v, level + 1) for k, v in obj.items()])
            + INDENT * level
            + "}"
        )

    if isinstance(obj, list):
        obj = cast(List[Any], obj)
        name = type(obj).__name__

        if name != "list":
            name += "(list)"

        if len(obj) == 0:
            return name + " []"

        return (
            name
            + " [\n"
            + "".join([_inspect_list_item(v, level + 1) for v in obj])
            + INDENT * level
            + "]"
        )

    if isinstance(obj, tuple):
        obj = cast(Tuple[Any, ...], obj)
        name = type(obj).__name__

        if name != "tuple":
            name += "(tuple)"

        if len(obj) == 0:
            return name + " ()"

        return (
            name
            + " (\n"
            + "".join([_inspect_list_item(v, level + 1) for v in obj])
            + INDENT * level
            + ")"
        )

    if len([k for k in dir(obj) if not k.startswith("_")]) == 0:
        return type(obj).__name__ + "+{}"

    return (
        type(obj).__name__
        + "+{\n"
        + "".join(
            [
                INDENT * (level + 1)
                + k
                + ": "
                + _inspect(getattr(obj, k), level + 1)
                + ",\n"
                for k in dir(obj)
                if not k.startswith("_")
            ]
        )
        + INDENT * level
        + "}"
    )


def inspect(obj: object) -> None:
    print(_inspect(obj, 0))
