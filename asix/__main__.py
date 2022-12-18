import sys
from os import chdir, mkdir

from asix import fs
from asix.fs import GUEST, ROOT
from asix.errors import StopProgram
from asix.config import Config

# sys.tracebacklimit = 0

config = Config.load(sys.argv[1])
chdir(config.dirname)

if config.out_debug_branches_graph_dir:
    try:
        mkdir(config.out_debug_branches_graph_dir)
    except FileExistsError:
        pass

    fs.branches_graph_dir = config.out_debug_branches_graph_dir

for k, v in config.setup_copy.items():
    with open(v, "rt") as f:
        fs.write_file(k, f.read(), ROOT)

for k, v in config.setup_write.items():
    fs.write_file(k, v, ROOT)

for k, v in config.setup_append.items():
    fs.append_file(k, v, ROOT)

for k, (perm, follow_symlinks) in config.setup_permissions.items():
    fs.change_perm(k, GUEST, perm, ROOT, follow_symlinks)

try:
    for p in config.init:
        status = fs.execute_file(p, ROOT)
        if status:
            exit(status)
except StopProgram:
    exit(1)

for k, v in config.out_copy.items():
    with open(k, "wt") as f:
        f.write(fs.read_file(v, ROOT))
