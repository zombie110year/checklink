from queue import Queue, Empty
from threading import Thread
from typing import NewType, Tuple

from ..parse import Link


class Reporter(Thread):
    def __init__(self, results: "Queue[Link, bool]"):
        super().__init__()
        self.__results = results

    @property
    def results(self):
        return self.__results


class CommandLineReporter(Reporter):

    def run(self):
        while True:
            try:
                link, reachable = self.results.get(True, 3)
            except Empty:
                break
            if reachable:
                # string = f"\x1b[32m{link.location} {link.url}\x1b[0m"
                pass
            else:
                string = f"\x1b[31m{link.location} {link.url}\x1b[0m"
                print(string)
