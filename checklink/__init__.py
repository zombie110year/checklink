"""死链检查
"""

from .markdown import run
from argparse import ArgumentParser

def getParser():

    parser = ArgumentParser(
        prog="checklink",
        description="check link connectability recursely"
    )
    parser.add_argument(
        "path", default=".", help="what directory will be check",
    )
    parser.add_argument(
        "-t", "--target", default="md", help="which type the file is",
        choices=['md']
    )

    return parser

def main():
    parser = getParser()
    args = parser.parse_args()
    if args.target == "md":
        run(args.path)
    elif args.target == "rst":
        pass
    else:
        print("invalid target")
