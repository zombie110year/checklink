from checklink import __version__
from checklink.parse.markdown import MarkdownParser


def test_version():
    assert __version__ == "0.1.0"


class TestMarkdown:
    @classmethod
    def setup_class(cls):
        cls.parser = MarkdownParser()

    def test_single_link(self):
        link = self.parser.parse("[你好世界](https://example.com/)")[0]
        assert link.url == "https://example.com/"
        assert link.path == "<not a file>"
        assert link.row == 1
        assert link.column == 0

    def test_single_image_link(self):
        link = self.parser.parse("![你好世界](https://example.com/)")[0]
        assert link.url == "https://example.com/"
        assert link.path == "<not a file>"
        assert link.row == 1
        assert link.column == 0

    def test_find_links(self):
        links = self.parser.parse(
            "example.com [a](a), jfkadsi [b](b) kaadf ![ka](ak) ,a.fn.")
        assert len(links) == 3
        a, b, c = links
        assert a.url == "a"
        assert b.url == "b"
        assert c.url == "ak"

    def test_invalid_chars(self):
        link = self.parser.parse("[](https:// kkkk.com)")[0]
        assert link.url == "https:// kkkk.com"

    def test_file(self):
        links = self.parser.parse_file("tests/sample-markdown.md")
        assert len(links) == 2
        a, b = links
        assert a.url == "https://example.com"
        assert a.path == "tests/sample-markdown.md"
        assert a.row == 5
        assert b.url == "./local/static/sample.png"
        assert b.row == 7
