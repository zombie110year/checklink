from queue import Queue

from pytest import fixture

from checklink.check import HTTPChecker, LocalChecker
from checklink.parse import Link


@fixture(scope="function")
def links():
    return Queue()


@fixture(scope="function")
def results():
    return Queue()


def test_http_check(links, results):
    links.put(
        Link("https://no-one-will-all-this-name-fjksgua.com", "<string>", 0, 0))
    links.put(Link("https://www.bilibili.com", "<string>", 0, 0))
    checker = HTTPChecker(links, results)
    checker.start()
    checker.join()
    a = results.get()
    b = results.get()
    assert a[1] == False
    assert b[1] == True


def test_local_check(links, results):
    links.put(Link("tests/sample-markdown.md", "<string>", 0, 0))
    links.put(Link("C:/Users/bill-gates", "<string>", 0, 0))
    checker = LocalChecker(links, results)
    checker.start()
    checker.join()
    a = results.get()
    b = results.get()
    assert a[1] == True
    assert b[1] == False
