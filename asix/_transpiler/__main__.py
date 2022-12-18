from escodegen import generate # type: ignore
from . import process_module, from_file
from sys import argv

mod = process_module(from_file(argv[1]), argv[1])

print(generate(mod.get())) # type: ignore
