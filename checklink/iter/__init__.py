from pathlib import Path
from threading import Thread
from queue import Queue, Empty
from typing import Generator, Tuple


class Iter(Thread):
    def __init__(self, get: Queue, put: Queue):
        super().__init__()
        self.__get = get
        self.__put = put

    def run(self):
        while True:
            try:
                item = self.__get.get(True, 3)
            except Empty:
                break
            result = self.product(item)
            for i in result:
                self.__put.put(i)

    def product(self, obj):
        return (obj, )


class FileIter(Iter):
    def __init__(self, get: Queue, put_dir: Queue, put_file: Queue):
        Thread.__init__(self)
        self.__get = get
        self.__put_dir = put_dir
        self.__put_file = put_file

    def run(self):
        while True:
            try:
                item = self.__get.get(True, 3)
            except Empty:
                break
            result = self.product(item)
            for i in result:
                if i.is_file():
                    self.__put_file.put(i)
                elif i.is_dir():
                    self.__put_dir.put(i)

    def product(self, obj: "directory") -> Generator[None, None, Path]:
        yield from obj.iterdir()


class TextIter(Iter):

    def product(self, obj: Path) -> Tuple[str]:
        return (obj.read_text("utf-8"), )
