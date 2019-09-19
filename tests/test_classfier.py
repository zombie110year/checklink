"""URL 分类器
"""

from checklink.workers import classify

def test_url_classfier():
    assert classify("https://example.com") == "http"
    assert classify(".local/static/sample.png") == "local"
