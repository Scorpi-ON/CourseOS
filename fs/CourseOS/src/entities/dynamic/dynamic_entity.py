from abc import abstractmethod
from typing import BinaryIO, Self, TypeVar

from CourseOS.src.entities.entity import Entity

T = TypeVar("T", bound="DynamicEntity")


class DynamicEntity(Entity):
    def write(self, buf: BinaryIO, pos: int | None = None) -> None:
        raise NotImplementedError

    @classmethod
    def read(cls, buf: BinaryIO, pos: int | None = None) -> Self:
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls: type[T], bytes_: bytes) -> list[T]:
        pass

    @classmethod
    def to_bytes(cls, objects: list[T]) -> bytes:
        return b"\n".join(bytes(obj) for obj in objects)
