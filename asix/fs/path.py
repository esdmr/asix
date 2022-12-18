from typing import TYPE_CHECKING, Generator, List, Optional, Union
from .dir import FSDir

from .symlink import FSSymlink
from .utils import FSEntry, get_generator_value

if TYPE_CHECKING:
    from .root import FS


__all__ = ["FSPath", "FSRelPath", "FSAnyPath", "get_path"]


class FSPath(str):
    class Initial:
        def __init__(self, root: "FS", proc: int) -> None:
            self.dirname = FSPath("/")
            self.basename = "/"
            self.root = root
            self.parent = root
            self.proc = proc

        @property
        def entry(self) -> "FS":
            return self.root

        @entry.setter
        def entry(self, entry: FSEntry) -> None:
            raise RuntimeError("Cannot set root")

        @entry.deleter
        def entry(self) -> None:
            raise RuntimeError("Cannot delete initial component")

    class Medial:
        def __init__(
            self,
            dirname: "FSPath",
            basename: str,
            root: "FS",
            parent: "FSDir",
            proc: int,
        ):
            assert dirname.endswith(
                "/"
            ), f"Directory name “{dirname}” of medial entry “{basename}” does not end with slash"
            self.dirname = dirname
            self.basename = basename
            self.root = root
            self.parent = parent
            self.proc = proc

        @property
        def entry(self) -> "FSDir":
            entry: Optional[FSEntry] = self.parent.get_entry(self.basename, self.proc)
            path = FSPath(self.dirname + self.basename)
            resolved_path = path

            try:
                while isinstance(entry, FSSymlink):
                    resolved_path = entry.get_target(self.proc).to_absolute(
                        self.dirname
                    )
                    entry = resolved_path.get_result(self.root, self.proc).entry
            except Exception as e:
                raise RuntimeError(f"Error while resolving “{path}” symlink") from e

            resolution = (
                " " if path == resolved_path else f" — resolved as “{resolved_path}” — "
            )
            assert isinstance(
                entry, FSDir
            ), f"Path “{path}”{resolution}is not a directory"
            return entry

        @entry.setter
        def entry(self, entry: "FSDir") -> None:
            self.parent.set_entry(self.basename, entry, self.proc)

        @entry.deleter
        def entry(self) -> None:
            raise RuntimeError("Cannot delete medial component")

    class Final:
        def __init__(
            self,
            dirname: "FSPath",
            basename: str,
            root: "FS",
            parent: "FSDir",
            proc: int,
            has_slash: bool,
        ):
            assert dirname.endswith(
                "/"
            ), f"Directory name “{dirname}” of final entry “{basename}” does not end with slash"
            self.dirname = dirname
            self.basename = basename
            self.root = root
            self.parent = parent
            self.proc = proc
            self.has_slash = has_slash

        def __validate_entry(self, entry: Optional[FSEntry]) -> None:
            if not self.has_slash or not entry:
                return

            path = FSPath(self.dirname + self.basename)
            resolved_path = path

            try:
                while isinstance(entry, FSSymlink):
                    resolved_path = entry.get_target(self.proc).to_absolute(
                        self.dirname
                    )
                    entry = resolved_path.get_result(self.root, self.proc).entry
            except Exception as e:
                raise RuntimeError(f"Error while resolving “{path}” symlink") from e

            resolution = (
                " " if path == resolved_path else f" — resolved as “{resolved_path}” — "
            )
            assert isinstance(
                entry, FSDir
            ), f"Path “{path}”{resolution}is not a directory"

        @property
        def entry(self) -> Optional[FSEntry]:
            entry = self.parent.get_entry(self.basename, self.proc)
            self.__validate_entry(entry)
            return entry

        @entry.setter
        def entry(self, entry: FSEntry) -> None:
            self.__validate_entry(entry)
            self.parent.set_entry(self.basename, entry, self.proc)

        @entry.deleter
        def entry(self) -> None:
            self.__validate_entry(None)
            self.parent.set_entry(self.basename, None, self.proc)

    Component = Union[Initial, Medial, Final]
    Result = Union[Initial, Final]

    def __get_parts(self) -> List[str]:
        out: List[str] = []

        for name in self.split("/"):
            if name == "..":
                try:
                    out.pop()
                except IndexError:
                    pass
            elif name or name == ".":
                out.append(name)

        return out

    def to_absolute(self, base: "FSPath") -> "FSPath":
        return self

    def iterate(self, root: "FS", proc: int) -> Generator[Component, None, Result]:
        assert self.startswith("/"), f"FSPath {self} is not an absolute path"
        initial = self.Initial(root, proc)
        yield initial

        if self.startswith("/str/"):
            medial = self.Medial(FSPath("/"), "str", root, root, proc)
            yield medial
            final = self.Final(
                FSPath("/str/"), self[5:], root, medial.entry, proc, False
            )
            yield final
            return final

        names = self.__get_parts()
        final_slash = self.endswith("/")

        try:
            final_name = names.pop()
        except IndexError:
            return initial

        parent: FSDir = root
        dirname = FSPath("/")

        for medial_name in names:
            medial = self.Medial(dirname, medial_name, root, parent, proc)
            yield medial
            parent = medial.entry
            dirname = FSPath(dirname + medial_name + "/")

        final = self.Final(dirname, final_name, root, parent, proc, final_slash)
        yield final
        return final

    def get_result(self, root: "FS", proc: int) -> Result:
        return get_generator_value(self.iterate(root, proc))

    def get_dirname(self) -> "FSPath":
        if self.startswith("/str/"):
            return FSPath("/str")

        return FSPath("/" + "/".join(self.__get_parts()[0:-1]) + "/")


class FSRelPath(str):
    def to_absolute(self, base: FSPath) -> FSPath:
        return FSPath(f"{base}/{self}")


FSAnyPath = Union[FSPath, FSRelPath]


def get_path(path: str) -> FSAnyPath:
    return FSPath(path) if path.startswith("/") else FSRelPath(path)
