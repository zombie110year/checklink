"""All multi thread workers

- HTTPChecker
- LocalChecker
- FileIter
- TextIter
- MarkdownParseWorker

"""

from queue import Empty, Queue
from threading import Thread

from ..check import HTTPChecker, LocalChecker
from ..iter import FileIter, TextIter
from ..parse import Link
from ..parse.markdown import MarkdownParser


class MarkdownParseWorker(Thread):
    def __init__(self, files: Queue, http_links: Queue, local_links: Queue):
        super().__init__()
        self.__files = files
        self.__http = http_links
        self.__local = local_links
        self.parser = MarkdownParser()

    def run(self):
        while True:
            try:
                path = self.__files.get(True, 3)
            except Empty:
                break

            for i in self.parser.parse_file(str(path)):
                if HTTPChecker.URL_MATCH.fullmatch(i.url):
                    self.__http.put(i)
                elif LocalChecker.URL_MATCH.fullmatch(i.url):
                    self.__local.put(i)
