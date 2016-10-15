#!/usr/bin/env python

from __future__ import print_function

import re
import os
import os.path
from sys import argv


EXCLUDES = ['implementation', 'testbench']
BASIC_ID_REGEX = (
    r'[a-z]'            # a basic identifier starts with an alphabetic char
    r'[a-z0-9]*'        # it can contain alphanumerics
    r'(?:_[a-z0-9]+)*'  # and '_' but not at the end
)


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
    instantiation_regex = (
        r'\s*'               # indentation
        r'(?P<entity>{0})'   # single basic identifier
        r'\s*:\s*entity\s*'  # entity declaration and spacing
        r'(?P<component>'    # component:
           r'{0}'            # at least a basic identifier
           r'(?:\.{0})*'     # for libraries: dots can only appear if they are followed by another basic identifier # NOQA
        r')'
        .format(BASIC_ID_REGEX)
)
    p = re.compile(instantiation_regex, re.IGNORECASE)
    vhd_files = dict(find_vhd(proot))
    for level, entity, path in _vhdltree(0, filepath, p, vhd_files):
        print('{indent}{entity} : {path}'.format(indent=4*' '*level,
                                                 entity=entity,
                                                 path=path or 'Not found'))


if __name__ == '__main__':
    vhdltree(argv[1], argv[2])
