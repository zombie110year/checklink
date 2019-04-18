"""递归查找目录下的 md/rst 文件中的死链, 返回文件路径以及行号
"""

import re
from pathlib import Path

import requests as r

from .re_ import MD_LINK, removeAnchor, HTTP_URL, PATH
from .formatter_ import MessageFormatter

class MarkdownFinder:

    def __init__(self, root):
        self._suffix = {".md", ".MD", ".markdown"}
        self._formatter = MessageFormatter("{}:{} {}")
        self._pattern = MD_LINK
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
                    url = match.groupdict()['url']
                    if not url is None:
                        self.testLink(match.group("url"), path, i)
                    else:
                        self._formatter(path, i, "None")

    def testLink(self, link_url, file_path, line_num):
        if HTTP_URL.match(link_url):   # 网络地址
            x = HTTP_URL.match(link_url)
            url = removeAnchor(x)

            try:
                response = r.get(url)
            except r.ConnectionError:
                self._formatter(file_path.absolute(), line_num, link_url)
                return

            if response.status_code in [403, 404, 408]: # 出问题了
                self._formatter(file_path.absolute(), line_num, link_url)
        elif PATH.match(link_url):# 本地路径
            x = PATH.match(link_url)
            link_url = x.group('path')
            if link_url[0] == '/':
                x = Path(link_url[1:])
                path = self._root / x
            else:
                x = Path(link_url)
                path = file_path.parent / x
            if not path.exists():
                self._formatter(file_path.absolute(),
                line_num, link_url)
        else:
            self._formatter(file_path.absolute(), line_num, link_url[:20])

    def run(self):
        self.walk(self._root)
