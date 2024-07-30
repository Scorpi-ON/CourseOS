import conf
import tools
from entities.entity import Entity


class Block(Entity):
    size = conf.BLOCK_SIZE

    @classmethod
    def _get_attrs(cls):
        return ('_bytes',)

    def __init__(
            self,
            size: int | None = None,
            bytes_: bytes | bytearray | None = None
    ):
        assert size and not bytes_ or bytes_ and not size
        self._bytes = bytearray(size if size else bytes_)

    def write(self, buf, pos=None):
        tools.seek_if_pos(buf, pos)
        buf.write(self._bytes)

    @classmethod
    def read(cls, buf, pos=None):
        tools.seek_if_pos(buf, pos)
        return Block(bytes_=buf.read(Block.size))
