#!/usr/bin/env python

import re
from sys import argv
from os import walk
from os.path import join as pjoin


EXCLUDES = ["implementation", "testbench"]
BASIC_ID_REGEX = "[a-z][a-z0-9]*(?:_[a-z0-9]+)*"


def _vhdltree(level, filepath, pattern, vhd_files):
    included_entities = find_entities(filepath, pattern)
    if included_entities:
        for entity, component in included_entities.items():
            path = vhd_files.get(component.lower())
            if path:
                print("    "*level + entity + " : " + path)
                _vhdltree(level+1, path, pattern, vhd_files)
            else:
                print("    "*level + entity + " : Not Found")


def find_entities(filepath, pattern):
    included_entities = {}
    with open(filepath) as f:
        for l in f:
            m = pattern.match(l)
            if m:
                included_entities[m.group(1)] = m.group(2).split(".")[-1]
    return included_entities


def find_vhd(proot):
    vhd_files = {}
    for (dirpath, dirnames, filenames) in walk(proot):
        i, excluded = 0, False
        while i < len(EXCLUDES) and not excluded:
            excluded = EXCLUDES[i] in dirpath.lower()
            i += 1
        if not excluded:
            for n in filenames:
                l = n.split(".")
                ext = l[-1]
                if ext.lower() == "vhd":
                    basename = l[-2]
                    vhd_files[basename.lower()] = pjoin(dirpath, n)
    return vhd_files


def vhdltree(filepath, proot):
    instantiation_regex = ("\s*({0})\s*:\s*entity\s*({0}(?:\.{0})*)"
                           .format(BASIC_ID_REGEX))
    p = re.compile(instantiation_regex, re.IGNORECASE)
    vhd_files = find_vhd(proot)
    _vhdltree(0, filepath, p, vhd_files)

if __name__ == "__main__":
    vhdltree(argv[1], argv[2])
