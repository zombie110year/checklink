"""
Text Parsers to find url from content.

Every url item should contain:

- url
- location(`filepath:row:column`)
"""
from abc import abstractmethod
from typing import List


class Link:
    def __init__(self, url: str, path: str, row: int, column: int):
        """init link object

        :param str url: link's href
        :param str path: where found this link, file path
        :param int row: where found this link, line number
        :param int column: where found this link, chars after line beginning
        """
        self.__url = url
        self.__path = path
        self.__row = row
        self.__column = column

    @property
    def url(self) -> str:
        return self.__url

    @property
    def path(self) -> str:
        return self.__path

    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column

    @property
    def location(self) -> str:
        return f"{self.path}:{self.row}:{self.column}"

    @path.setter
    def path(self, other: str):
        self.__path = other
