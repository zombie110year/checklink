import unittest as t

from checklink.re_ import HTTP_URL, MD_LINK

markdown_link = [
    "[title](https://github.com)",
    "[t itl e](https://github.com/)",
    "[ title](https://github.com/zombie110year)",
    "[title ](https://github.com/zombie110year/)",
    "[](https://github.com/zombie110year/checklink)",
    "[title](https://github.com/zombie110year/checklink/)",
    "[标题](https://github.com/zombie110year/checklink#checklink)",
    "[](https://github.com/zombie110year/checklink/blob/master/README.md)",
    "['](https://github.com/zombie110year/checklink/blob/master/README.md#checklink)",
]

markdown_pic_link = [
    "![title](https://github.com)",
    "![t itl e](https://github.com/)",
    "![ title](https://github.com/zombie110year)",
    "![title ](https://github.com/zombie110year/)",
    "![](https://github.com/zombie110year/checklink)",
    "![title](https://github.com/zombie110year/checklink/)",
    "![标题](https://github.com/zombie110year/checklink#checklink)",
    "![](https://github.com/zombie110year/checklink/blob/master/README.md)",
    "!['](https://github.com/zombie110year/checklink/blob/master/README.md#checklink)",
]

url_answer = [
    "https://github.com",
    "https://github.com/",
    "https://github.com/zombie110year",
    "https://github.com/zombie110year/",
    "https://github.com/zombie110year/checklink",
    "https://github.com/zombie110year/checklink/",
    "https://github.com/zombie110year/checklink#checklink",
    "https://github.com/zombie110year/checklink/blob/master/README.md",
    "https://github.com/zombie110year/checklink/blob/master/README.md#checklink",
]

http_answer = [
    ("https://", "github.com", None, None),
    ("https://", "github.com", "/", None),
    ("https://", "github.com", "/zombie110year", None),
    ("https://", "github.com", "/zombie110year/", None),
    ("https://", "github.com", "/zombie110year/checklink", None),
    ("https://", "github.com", "/zombie110year/checklink/", None),
    ("https://", "github.com", "/zombie110year/checklink", "#checklink"),
    ("https://", "github.com", "/zombie110year/checklink/blob/master/README.md", None),
    ("https://", "github.com",
     "/zombie110year/checklink/blob/master/README.md", "#checklink"),
]


class TestRe_(t.TestCase):
    def setUp(self):
        pass

    def test_md_link(self):
        for q, a in list(zip(markdown_link, url_answer)):
            x = MD_LINK.match(q)
            self.assertEqual(
                x.group('url'), a, msg=q
            )
        for q, a in list(zip(markdown_pic_link, url_answer)):
            x = MD_LINK.match(q)
            self.assertEqual(
                x.group('url'), a, msg=q
            )

    def test_http_url(self):
        for q, a in list(zip(url_answer, http_answer)):
            x = HTTP_URL.match(q)
            self.assertEqual(
                x.group('protocol'), a[0], msg=q
            )
            self.assertEqual(
                x.group('domain'), a[1], msg=q
            )
            self.assertEqual(
                x.group('path'), a[2], msg=q
            )
            self.assertEqual(
                x.group('anchor'), a[3], msg=q
            )
