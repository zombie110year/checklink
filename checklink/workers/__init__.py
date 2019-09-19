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
from ..report import CommandLineReporter


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
                class_ = classify(i.url)
                if class_ == "local":
                    self.__local.put(i)
                elif class_ == "http":
                    self.__http.put(i)


def classify(url) -> str:
    if HTTPChecker.URL_MATCH.fullmatch(url):
        return "http"
    elif LocalChecker.URL_MATCH.fullmatch(url):
        return "local"
