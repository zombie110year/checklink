import unittest as t

from checklink.re_ import HTTP_URL, MD_LINK, PATH

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


path_list = [
    "/home/zombie110year/hello",
    "tests/__init__.py",
    "../example",
    "./.gitignore",
    ".gitignore",
]

path_list_error = [
    "mailto:zombie110year@outlook.com",
    "data:image/png,base64,jfkdajkfjkaslf;jadf",
]

path_ans = [
    "/home/zombie110year/hello",
    "tests/__init__.py",
    "../example",
    "./.gitignore",
    ".gitignore",
]

markdown_special_ans = [
    "/__init__.py",
    "mailto:zombie110year@outlook.com",
    "data:image/png;base64,ILENFLKSNGEJ",
    "#这是一个测试用文件",
    None,
    None,
    "https://github.com/",
    "__init__.py",
    "/__init__.py",
    "__main__.py",
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

    def test_path(self):
        for q, a in list(zip(path_list, path_ans)):
            x = PATH.match(q)
            self.assertEqual(x.group('path'), a)

        for q in path_list_error:
            x = PATH.match(q)
            self.assertEqual(x, None)


    def test_markdown_special(self):
        stack = []
        with open("tests/test_markdown.md", "rt", encoding="utf-8") as file:
            content = file.readlines()

        for line in content:
            x = MD_LINK.match(line)
            if x:
                stack.append(x.group('url'))

        for i, j in list(zip(stack, markdown_special_ans)):
            self.assertEqual(i, j)
