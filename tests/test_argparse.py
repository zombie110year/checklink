from checklink.cli import argparser

def test_argparser():
    parser = argparser()
    args = parser.parse_args([])
    assert args.root == "."
    assert args.checkers == 4
    args = parser.parse_args(["this"])
    assert args.root == "this"
    assert args.checkers == 4
    args = parser.parse_args(["-j", "100"])
    assert args.root == "."
    assert args.checkers == 100
    args = parser.parse_args(["there", "-j", "200"])
    assert args.root == "there"
    assert args.checkers == 200
