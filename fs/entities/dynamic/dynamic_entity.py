from abc import abstractmethod
import typing

from entities.entity import Entity


class DynamicEntity(Entity):
    def write(self, buf, pos=None):
        raise NotImplementedError()

    @classmethod
    def read(cls, buf, pos=None):
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls, bytes_: bytes) -> typing.List[typing.Self]:
        pass

    @classmethod
    def to_bytes(cls, objects: typing.List[typing.Self]) -> bytes:
        return b'\n'.join(bytes(obj) for obj in objects)
