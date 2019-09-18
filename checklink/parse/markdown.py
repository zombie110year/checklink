"""MarkdownParser
"""
from typing import List, Generic
import re
from . import Link, Parser


class MarkdownParser(Parser):
    PATTERN = re.compile(r"!?\[(?P<name>[^\]]*)\]\((?P<url>[^\)]+)\)")

    def parse(self, text: str, path: str = None) -> List[Link]:
        res = []
        if path is None:
            path = "<not a file>"
        for num, line in enumerate(re.split(r"\r?\n", text)):
            for i in self.findall(line):
                link = Link(i["url"], path, num + 1, i.span()[0])
                res.append(link)
            return res

    def parse_file(self, path: str) -> List[Link]:
        with open(path, "rt", encoding="utf-8") as file:
            text = file.read()
        return self.parse(text, path)

    def findall(self, text: str) -> Generic[re.Match]:
        for i in self.PATTERN.finditer(text):
            yield i
