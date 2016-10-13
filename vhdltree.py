#!/usr/bin/env python

import re
from sys import argv
from os import walk
from os.path import join as pjoin


EXCLUDES = ["implementation", "testbench"]
BASIC_ID_REGEX = "[a-z][a-z0-9]*(?:_[a-z0-9]+)*"


def _vhdltree(level, filepath, pattern, vhd_files):
    for entity, component in find_entities(filepath, pattern):
        path = vhd_files.get(component.lower(), "Not Found")
        print("    "*level + entity + " : " + path)
        if path != "Not Found":
            _vhdltree(level+1, path, pattern, vhd_files)


def find_entities(filepath, pattern):
    with open(filepath) as f:
        for l in f:
            m = pattern.match(l)
            if m:
                yield m.group('entity'), m.group('component').split(".")[-1]


def find_vhd(proot):
    for (dirpath, dirnames, filenames) in walk(proot):
        if all(excluder not in dirpath.lower() for excluder in EXCLUDES):
            for fn in filenames:
                if fn[-4:].lower() == ".vhd":
                    yield fn[:-4].lower(), pjoin(dirpath, fn)


def vhdltree(filepath, proot):
    instantiation_regex = ("\s*(?P<entity>{0})\s*:\s*entity\s*(?P<component>{0}(?:\.{0})*)"  # NOQA
                           .format(BASIC_ID_REGEX))
    p = re.compile(instantiation_regex, re.IGNORECASE)
    vhd_files = dict(find_vhd(proot))
    _vhdltree(0, filepath, p, vhd_files)

if __name__ == "__main__":
    vhdltree(argv[1], argv[2])
