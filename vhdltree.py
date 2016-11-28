#!/usr/bin/env python3

from __future__ import print_function

import re
import os
import argparse


EXCLUDES = ['implementation', 'testbench']
BASIC_ID_REGEX = (
    r'[a-z]'            # a basic identifier starts with an alphabetic char
    r'[a-z0-9]*'        # it can contain alphanumerics
    r'(?:_[a-z0-9]+)*'  # and '_' but not at the end
)
INSTANTIATION_REGEX = (
    r'\s*'               # indentation
    r'(?P<entity>{0})'   # single basic identifier
    r'\s*:\s*entity\s*'  # entity declaration and spacing
    r'(?P<component>'    # component:
        r'{0}'            # at least a basic identifier # noqa E131
        r'(?:\.{0})*'     # for libraries: dots can only appear if they are followed by another basic identifier
    r')'
    .format(BASIC_ID_REGEX)
)
INSTANTIATION_PATTERN = re.compile(INSTANTIATION_REGEX, re.IGNORECASE)


def _vhdltree(level, vhd_path, vhd_files):
    with open(vhd_path) as vhd_file:
        for entity, component in find_entities(vhd_file):
            try:
                path = vhd_files[component.lower()]
            except KeyError:
                yield level, entity, ''
            else:
                yield level, entity, path
                yield from _vhdltree(level + 1, path, vhd_files)


def find_entities(lines):
    for l in lines:
        m = INSTANTIATION_PATTERN.match(l)
        if m:
            yield m.group('entity'), m.group('component').split('.')[-1]


def find_vhd(directory):
    for entry in os.listdir(directory):
        entrypath = os.path.join(directory, entry)
        if os.path.isfile(entrypath) and entry[-4:].lower() == '.vhd':
                yield entry[:-4].lower(), entrypath
        elif os.path.isdir(entrypath):
            if all(excluder not in entry.lower() for excluder in EXCLUDES):
                yield from find_vhd(entrypath)


def vhdltree(filepath, proot):
    vhd_files = dict(find_vhd(proot))
    for level, entity, path in _vhdltree(0, filepath, vhd_files):
        print('{indent}{entity} : {path}'.format(indent=4 * ' ' * level,
                                                 entity=entity,
                                                 path=path or 'Not found'))


def parse_args():
    parser = argparse.ArgumentParser(description='A minimal tool to print'
                                     'the entity tree of a VHDL project',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('main', help='The main vhdl file')
    parser.add_argument('--project', '-p',
                        help='The project root directory',
                        default='./')
    args = parser.parse_args()
    return args.main, args.project


if __name__ == '__main__':
    vhd_main, proot = parse_args()
    vhdltree(vhd_main, proot)
