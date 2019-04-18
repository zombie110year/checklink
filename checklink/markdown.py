"""递归查找目录下的 md/rst 文件中的死链, 返回文件路径以及行号
"""

import re
from pathlib import Path
from queue import Queue, Empty
from threading import Thread

import requests as r

from .re_ import MD_LINK, removeAnchor, HTTP_URL, PATH
from .formatter_ import MessageFormatter


DIR_QUEUE = Queue(1024)     # Path
FILE_QUEUE = Queue(1024)    # Path
LINK_QUEUE = Queue(1024)    # (url: str, file: Path, line: int)
MSG_QUEUE = Queue(1024)     # str

POOL = []

_SUFFIX = {".md", ".MD", ".markdown"}
_FORMATTER = MessageFormatter("{}:{}\t{}")
_ROOT = Path()

RUNNING = {"displayMsg", "walk", "findLinkfromFile", "testLink"}


def init(root):
    global _ROOT
    _ROOT = Path(root).absolute()


def displayMsg():
    # 当且仅当 所有消息都发出去 并且 其他线程都停止才中断
    while ("testLink" in RUNNING) or (not MSG_QUEUE.empty()):
        msg = MSG_QUEUE.get()
        print(msg)

    RUNNING.discard("displayMsg")
    return

def walk():
    """一次循环就会找遍一个目录下的所有子对象, 如果 DIR_QUEUE 为空, 说明所有目录已被索引,
    即使有未完的文件, 也在 FILE_QUEUE 中.

    因此, 当 DIR_QUEUE 为空就可以停止此线程了.
    """
    while not DIR_QUEUE.empty():
        if not DIR_QUEUE.empty():
            crt = DIR_QUEUE.get()
            for file in crt.iterdir():
                if file.suffix in _SUFFIX and file.is_file():
                    FILE_QUEUE.put(file)
                elif file.is_dir():
                    DIR_QUEUE.put(file)

    # 所有目录已探索完毕
    RUNNING.discard("walk")
    return


def findLinkfromFile():
    """当 walk 仍在 run 时, 说明仍有新的文件可能被加入
    """
    while ("walk" in RUNNING) or (not FILE_QUEUE.empty()):
        if not FILE_QUEUE.empty():
            file = FILE_QUEUE.get()
            i = 0
            with file.open("rt", encoding="utf-8") as f:
                for line in f.readlines():
                    i += 1
                    match = MD_LINK.match(line)
                    if not match is None:
                        url = match.groupdict()['url']
                        if not url is None:
                            LINK_QUEUE.put((url, file, i))
                        else:  # 空链接
                            MSG_QUEUE.put(_FORMATTER(file, i, "None"))

    RUNNING.discard("findLinkfromFile")
    return


def testLink():
    """当 findLinkfromFile 仍在运行时, 说明仍可能有新的 link 被加入
    """
    while ("findLinkfromFile" in RUNNING) or (not LINK_QUEUE.empty()):
        if not LINK_QUEUE.empty():
            link, file, line = LINK_QUEUE.get()

            if HTTP_URL.match(link):   # 网络地址
                x = HTTP_URL.match(link)
                url = removeAnchor(x)

                try:
                    response = r.get(url)
                except r.ConnectionError:
                    MSG_QUEUE.put(_FORMATTER(file, line, link))
                    return

                if response.status_code in [403, 404, 408]:  # 出问题了
                    MSG_QUEUE.put(_FORMATTER(file, line, link))
            elif PATH.match(link):  # 本地路径
                x = PATH.match(link)
                link = x.group('path')
                if link[0] == '/':
                    x = Path(link[1:])
                    path = _ROOT / x
                else:
                    x = Path(link)
                    path = file.parent / x
                if not path.exists():
                    MSG_QUEUE.put(_FORMATTER(file, line, link))
            else:
                MSG_QUEUE.put(_FORMATTER(file, line, link[:20]))

    RUNNING.discard("testLink")
    return


def run(root):
    init(root)

    DIR_QUEUE.put(_ROOT)

    POOL.append(Thread(target=walk, name="walk"))
    POOL.append(Thread(target=findLinkfromFile, name="findlink"))
    POOL.append(Thread(target=testLink, name="testlink0"))
    POOL.append(Thread(target=testLink, name="testlink1"))
    POOL.append(Thread(target=displayMsg, name="display-msg"))

    for tr in POOL:
        tr.start()
