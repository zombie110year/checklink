"""Check a Link whether reachable"""

import re
import threading
from queue import Queue, Empty
from pathlib import Path

import requests


class Checker(threading.Thread):
    URL_MATCH = re.compile("")
    TIMEOUT = 3

    def __init__(self, urls: "Queue[Link]", results: "Queue[Link]"):
        """
        :param Queue urls: get url from
        :param Queue results: send result to
        """
        super().__init__()
        self.urls = urls
        self.results = results

    def reachable(self, url: str) -> bool:
        if self.URL_MATCH.fullmatch(url):
            return False
        else:
            return False

    def run(self):
        while True:
            try:
                link = self.urls.get(True, self.TIMEOUT)
            except Empty:
                break

            result = (link, self.reachable(link.url))
            self.results.put(result)


class HTTPChecker(Checker):
    """Check http url
    """
    URL_MATCH = re.compile(
        r"((?P<protocol>https?)://)(?P<domain>(www.)?([^:/]+))(?P<path>(/[^/#]*)+)?(?P<anchor>#.*)?")
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    def reachable(self, url: str) -> bool:
        try:
            resp = requests.get(url, timeout=self.TIMEOUT,
                                headers=self.HEADERS)
            return resp.status_code // 100 != 4
        except:
            return False


class LocalChecker(Checker):
    """Check Local File System"""
    URL_MATCH = re.compile(
        r"(?!#)(?<!(?P<protocol>file)(://))(?P<label>[A-Z]:)?(?P<path>(/?[^\\/:*?\"<>\|]+)+)")

    def reachable(self, url: str) -> bool:
        path = Path(url)
        return path.exists()
