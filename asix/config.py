from dataclasses import dataclass
from json import loads
from typing import Dict, List, Tuple
from os.path import dirname, basename

from .fs import FSPath, FSPerm


def to_perm(text: str) -> Tuple[FSPerm, bool]:
    text = text.upper()
    perm = FSPerm.NONE
    perm |= FSPerm.R if "R" in text else FSPerm.NONE
    perm |= FSPerm.W if "W" in text else FSPerm.NONE
    perm |= FSPerm.X if "X" in text else FSPerm.NONE
    return perm, not ("F" in text)


@dataclass(eq=False, frozen=True, kw_only=True)
class Config:
    dirname: str
    setup_copy: Dict[FSPath, str]
    setup_write: Dict[FSPath, str]
    setup_append: Dict[FSPath, str]
    setup_permissions: Dict[FSPath, Tuple[FSPerm, bool]]
    init: List[FSPath]
    out_copy: Dict[str, FSPath]
    out_debug_branches_graph_dir: str

    @staticmethod
    def load(path: str) -> "Config":
        if not path.endswith(".json"):
            init_path = FSPath("/bin/init")
            return Config(
                dirname=dirname(path),
                setup_copy={init_path: basename(path)},
                setup_write={},
                setup_append={},
                setup_permissions={},
                init=[init_path],
                out_copy={},
                out_debug_branches_graph_dir="",
            )

        with open(path) as f:
            data = f.read()

        obj = loads(data) or {}
        setup = obj.get("setup") or {}
        setup_copy = setup.get("copy") or {}
        setup_write = setup.get("write") or {}
        setup_append = setup.get("append") or {}
        setup_permissions = setup.get("permissions") or {}
        init = obj.get("init") or []
        out = obj.get("out") or {}
        out_copy = out.get("copy") or {}
        out_debug = out.get("debug") or {}
        out_debug_branches_graph_dir = out_debug.get("branches_graph_dir") or ""

        assert isinstance(obj, dict), "Expected config “obj” to be an object"
        assert isinstance(setup, dict), "Expected config “setup” to be an object"
        assert isinstance(
            setup_copy, dict
        ), "Expected config “setup.copy” to be an object"
        assert isinstance(
            setup_write, dict
        ), "Expected config “setup.write” to be an object"
        assert isinstance(
            setup_append, dict
        ), "Expected config “setup.append” to be an object"
        assert isinstance(
            setup_permissions, dict
        ), "Expected config “setup.permissions” to be an object"
        assert isinstance(init, list), "Expected config “init” to be an array"
        assert len(init) >= 1, "Expected config “init” to have at least one entry"
        assert isinstance(out, dict), "Expected config “out” to be an object"
        assert isinstance(out_copy, dict), "Expected config “out.copy” to be an object"
        assert isinstance(
            out_debug, dict
        ), "Expected config “out.debug” to be an object"
        assert isinstance(
            out_debug_branches_graph_dir, str
        ), "Expected config “out.debug.branches_graph_dir” to be a string"

        return Config(
            dirname=dirname(path),
            setup_copy={FSPath(k): v for k, v in setup_copy.items()},
            setup_write={FSPath(k): v for k, v in setup_write.items()},
            setup_append={FSPath(k): v for k, v in setup_append.items()},
            setup_permissions={
                FSPath(k): to_perm(v) for k, v in setup_permissions.items()
            },
            init=[FSPath(p) for p in init],
            out_copy={k: FSPath(v) for k, v in out_copy.items()},
            out_debug_branches_graph_dir=out_debug_branches_graph_dir,
        )
