from argparse import ArgumentParser

from .main import main


def argparser():
    parser = ArgumentParser("checklink")
    parser.add_argument("root", nargs="?", const=".", default=".")
    parser.add_argument("-j", dest="checkers", type=int, required=False, default=32)
    return parser


def cli():
    args = argparser().parse_args()
    main(args.root, args.checkers)
