from .workers import HTTPChecker, LocalChecker, FileIter, MarkdownParseWorker, CommandLineReporter
from queue import Queue
from pathlib import Path


def main(root: str, checkers: int = 32):
    """start main processing

    :param int checkers: amount of HTTPCheck, Other Threads hava fix value.
    """
    dirs = Queue()
    files = Queue()
    http_links = Queue()
    local_links = Queue()
    results = Queue()
    dirs.put(Path(root))

    file_iters = [FileIter(dirs, dirs, files) for _ in range(4)]
    markdown_parsers = [MarkdownParseWorker(
        files, http_links, local_links) for _ in range(4)]
    http_checkers = [HTTPChecker(http_links, results) for _ in range(checkers)]
    local_checkers = [LocalChecker(local_links, results) for _ in range(1)]
    reporter = CommandLineReporter(results)

    for i in file_iters:
        i.start()
    for i in markdown_parsers:
        i.start()
    for i in local_checkers:
        i.start()
    for i in http_checkers:
        i.start()
    reporter.start()

    reporter.join()
    for i in http_checkers:
        i.join()
    for i in local_checkers:
        i.join()
    for i in markdown_parsers:
        i.join()
    for i in file_iters:
        i.join()
