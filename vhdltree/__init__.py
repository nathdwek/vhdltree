import argparse

from vhdltree.logic import vhdltree


def main():
    parser = argparse.ArgumentParser(
        description='A minimal tool to print the entity tree of a VHDL project',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('main', help='The main vhdl file')
    parser.add_argument(
        '--project', '-p',
        help='The project root directory',
        default='./'
    )
    args = parser.parse_args()
    vhdltree(args.main, args.project)
