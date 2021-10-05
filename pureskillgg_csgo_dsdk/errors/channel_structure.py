"""Exceptions for the csgo dsdk"""
from typing import List


class UnsupportedChannelStructure(Exception):
    """Exception raised for missing a column"""


class MissingColumns(UnsupportedChannelStructure):
    """Exception raised for missing a column"""

    def __init__(self, message: str, /, *, columns: List[str]):
        self.columns = columns
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f"{self._message}: missing columns {', '.join(self.columns)}"
