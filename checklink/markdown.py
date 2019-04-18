"""递归查找目录下的 md/rst 文件中的死链, 返回文件路径以及行号
"""

import re
from pathlib import Path

import requests as r

from .re_ import MD_LINK, removeAnchor, HTTP_URL
from .formatter_ import MessageFormatter

class MarkdownFinder:

    def __init__(self, root):
        self._suffix = {".md", ".MD", ".markdown"}
        self._formatter = MessageFormatter("{}:{} {}")
        self._pattern = re.compile(
            r"!?\[.*?\]\((?P<url>\S+)\)"
        )
        self._root = Path(root).absolute()

    def walk(self, root_dir: Path):
        crt = Path(root_dir)
        for file in crt.iterdir():
            if file.suffix in self._suffix and file.is_file():
                self.testFile(file)
            elif file.is_dir():
                self.walk(file)

    def testFile(self, path):
        i = 0
        with path.open("rt", encoding="utf-8") as file:
            for line in file.readlines():
                i += 1
                match = self._pattern.match(line)
                if not match is None:
                    self.testLink(match.group("url"), path, i)

    def testLink(self, link_url, file_path, line_num):
        x = HTTP_URL.match(link_url)
        if not x is None:   # 网络地址
            url = removeAnchor(x)
            response = r.get(url)
            if response.status_code != 200:
                self._formatter(file_path.absolute(), line_num, link_url)
        else: # 本地路径
            if link_url[0] == '/':
                x = Path(link_url[1:])
                path = self._root / x
            else:
                x = Path(link_url)
                path = file_path.parent / x
            if not path.exists():
                self._formatter(file_path.absolute(),
                line_num, link_url)

    def run(self):
        self.walk(self._root)
