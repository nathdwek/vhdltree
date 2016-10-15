#!/usr/bin/env python

from __future__ import print_function

import re
import os
import os.path
from sys import argv


EXCLUDES = ['implementation', 'testbench']
BASIC_ID_REGEX = '[a-z][a-z0-9]*(?:_[a-z0-9]+)*'


def _vhdltree(level, filepath, pattern, vhd_files):
    for entity, component in find_entities(open(filepath), pattern):
        try:
            path = vhd_files[component.lower()]
        except KeyError:
            yield level, entity, ''
        else:
            yield level, entity, path
            for l, e, p in _vhdltree(level+1, path, pattern, vhd_files):
                yield l, e, p


def find_entities(lines, pattern):
    for l in lines:
        m = pattern.match(l)
        if m:
            yield m.group('entity'), m.group('component').split('.')[-1]


def find_vhd(directory):
    for entry in os.listdir(directory):
        entrypath = os.path.join(directory, entry)
        if os.path.isfile(entrypath) and entry[-4:].lower() == '.vhd':
                yield entry[:-4].lower(), entrypath
        elif os.path.isdir(entrypath):
            if all(excluder not in entry.lower() for excluder in EXCLUDES):
                for component, path in find_vhd(entrypath):
                    yield component, path


def vhdltree(filepath, proot):
    instantiation_regex = ('\s*(?P<entity>{0})\s*:\s*entity\s*(?P<component>{0}(?:\.{0})*)'  # NOQA
                           .format(BASIC_ID_REGEX))
    p = re.compile(instantiation_regex, re.IGNORECASE)
    vhd_files = dict(find_vhd(proot))
    for level, entity, path in _vhdltree(0, filepath, p, vhd_files):
        print(' '*4*level, entity, ' : ', path or 'Not found')


if __name__ == '__main__':
    vhdltree(argv[1], argv[2])
