#!/usr/bin/env python

import re
import os
import os.path
from sys import argv

EXCLUDES = ["implementation", "testbench"]
BASIC_ID_REGEX = "[a-z][a-z0-9]*(?:_[a-z0-9]+)*"


def _vhdltree(level, filepath, pattern, vhd_files):
    for entity, component in find_entities(open(filepath), pattern):
        try:
            path = vhd_files[component.lower()]
        except KeyError:
            yield level, entity, "Not found"
        else:
            yield level, entity, path
            for l, e, p in _vhdltree(level+1, path, pattern, vhd_files):
                yield l, e, p


def find_entities(lines, pattern):
    for l in lines:
        m = pattern.match(l)
        if m:
            yield m.group('entity'), m.group('component').split(".")[-1]


def find_vhd(proot):
    for (dirpath, _, filenames) in os.walk(proot):
        if all(excluder not in dirpath.lower() for excluder in EXCLUDES):
            for fn in filenames:
                if fn[-4:].lower() == ".vhd":
                    yield fn[:-4].lower(), os.path.join(dirpath, fn)


def vhdltree(filepath, proot):
    instantiation_regex = ("\s*(?P<entity>{0})\s*:\s*entity\s*(?P<component>{0}(?:\.{0})*)"  # NOQA
                           .format(BASIC_ID_REGEX))
    p = re.compile(instantiation_regex, re.IGNORECASE)
    vhd_files = dict(find_vhd(proot))
    for level, entity, path in _vhdltree(0, filepath, p, vhd_files):
        print("    "*level + entity + " : " + path)

if __name__ == "__main__":
    vhdltree(argv[1], argv[2])
