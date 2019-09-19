from checklink.check import HTTPChecker, LocalChecker

def test_check_http_regex():
    pattern = HTTPChecker.URL_MATCH
    assert pattern.fullmatch("https://google.com")
    assert pattern.fullmatch("https://zombie110year.top/")
    assert pattern.fullmatch("https://zombie110year.top/2019/")
    assert pattern.fullmatch("https://zombie110year.top/#README")
    assert pattern.fullmatch("http://zombie110year.top/2019/#README")
    assert pattern.fullmatch("www.bilibili.com")
    assert pattern.fullmatch("www.bilibili.com/video/")
    assert not pattern.fullmatch("htp://kjfa.comaq/kda")
    assert not pattern.fullmatch("ttp://kjfa.comaq/kda")


def test_check_local_regex():
    pattern = LocalChecker.URL_MATCH
    assert pattern.fullmatch("hello.txt")
    assert pattern.fullmatch("./hello.txt")
    assert pattern.fullmatch("../hello.txt")
    assert pattern.fullmatch("./hello/echo.txt")
    assert pattern.fullmatch("C:/Users/zombie110year")
    assert pattern.fullmatch("/home/zombie110year")
    assert not pattern.fullmatch("/C:/Users/zombie110year")
    assert not pattern.fullmatch("file:///C:/Users/zombie110year/")
