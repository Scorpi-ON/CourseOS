from typing import BinaryIO

from CourseOS.src import conf, tools
from CourseOS.src.entities.entity import Entity


class Block(Entity):
    size = conf.BLOCK_SIZE

    @classmethod
    def _get_attrs(cls) -> tuple[str, ...]:
        return ("_bytes",)

    def __init__(self, size: int | None = None, bytes_: bytes | bytearray | None = None) -> None:
        assert (size and not bytes_) or (bytes_ and not size)
        self._bytes = bytearray(size if size else bytes_)  # type: ignore[arg-type]

    def write(self, buf: BinaryIO, pos: int | None = None) -> None:
        tools.seek_if_pos(buf, pos)
        buf.write(self._bytes)

    @classmethod
    def read(cls, buf: BinaryIO, pos: int | None = None) -> "Block":
        tools.seek_if_pos(buf, pos)
        return Block(bytes_=buf.read(Block.size))
