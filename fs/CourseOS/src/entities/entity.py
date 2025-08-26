import builtins
from abc import ABC, abstractmethod
from typing import BinaryIO, Self, TypeVar

T = TypeVar("T", bound="Entity")


class Entity(ABC):  # noqa: PLW1641
    @classmethod
    @abstractmethod
    def _get_attrs(cls) -> tuple[str, ...]:
        pass

    @abstractmethod
    def write(self, buf: BinaryIO, pos: int | None = None) -> None:
        pass

    @classmethod
    def read(cls, buf: BinaryIO, pos: int | None = None) -> Self:
        pass

    def __eq__(self, other: builtins.object) -> bool:
        for attr in self._get_attrs():
            if not hasattr(other, attr) or getattr(self, attr) != getattr(other, attr):
                return False
        return True
