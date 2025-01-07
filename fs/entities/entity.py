import typing
from abc import ABC, abstractmethod


class Entity(ABC):
    @classmethod
    @abstractmethod
    def _get_attrs(cls) -> typing.Tuple[str]:
        pass

    @abstractmethod
    def write(self, buf: typing.BinaryIO, pos: int = None):
        pass

    @classmethod
    @abstractmethod
    def read(cls, buf: typing.BinaryIO, pos: int = None) -> typing.Self:
        pass

    def __eq__(self, other: typing.Self) -> bool:
        for attr in self._get_attrs():
            if not hasattr(other, attr) or getattr(self, attr) != getattr(other, attr):
                return False
        return True
