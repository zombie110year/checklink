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
    def __init__(self, files: Queue, links: Queue):
        super().__init__()
        self.__files = files
        self.__links = links
        self.parser = MarkdownParser()

    def run(self):
        while True:
            try:
                path = self.__files.get(True, 3)
            except Empty:
                break

            for i in self.parser.parse_file(str(path)):
                self.__links.put(i)
