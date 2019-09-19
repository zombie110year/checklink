from argparse import ArgumentParser

from .main import main
from . import __version__


def argparser():
    parser = ArgumentParser("checklink")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("root", nargs="?", const=".", default=".")
    parser.add_argument("-j", dest="checkers", type=int, required=False, default=4)
    return parser


def cli():
    args = argparser().parse_args()
    main(args.root, args.checkers)
