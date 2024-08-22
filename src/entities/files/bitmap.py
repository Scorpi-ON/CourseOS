import typing

from src import conf, tools
from src.entities.files.block import Block


class Bitmap(Block):
    @staticmethod
    def _bits_to_bytes(bits: bytes | bytearray) -> bytearray:
        assert len(bits) % conf.BITS_IN_BYTE == 0 \
               and set(bits).issubset({0, 1})
        bytes_ = bytearray()
        for num in range(0, len(bits) - 1, conf.BITS_IN_BYTE):
            bytes_.append(
                int(''.join(map(str, bits[num:num + conf.BITS_IN_BYTE])), 2)
            )
        return bytes_

    def __init__(
            self,
            bit_count: int | None = None,
            bits: bytes | bytearray | None = None,
            bytes_: bytes | bytearray | None = None
    ):
        assert (
            bit_count and not (bits or bytes_)
            or bits and not (bit_count or bytes_)
            or bytes_ and not (bit_count or bits)
        )
        size = None
        if bit_count:
            assert bit_count % conf.BITS_IN_BYTE == 0
            size = bit_count // conf.BITS_IN_BYTE
        elif bits:
            bytes_ = Bitmap._bits_to_bytes(bits)
        super().__init__(size, bytes_)

    @property
    def size(self):
        return len(self._bytes)

    def __len__(self):
        return self.size * conf.BITS_IN_BYTE

    def _index_helper(self, index: int) -> typing.Tuple[int, int]:
        assert 0 <= index < len(self)
        byte_index = index >> conf.BITS_IN_BYTE_DEG
        bit_index = index % conf.BITS_IN_BYTE
        bit_index_reversed = conf.BITS_IN_BYTE - 1 - bit_index
        return byte_index, bit_index_reversed

    def __getitem__(self, index: int) -> int:
        byte_index, bit_index_reversed = self._index_helper(index)
        return self._bytes[byte_index] >> bit_index_reversed & 1

    def __setitem__(self, index: int, bit: int):
        assert bit in (0, 1)
        byte_index, bit_index_reversed = self._index_helper(index)
        if bit != self._bytes[byte_index] >> bit_index_reversed & 1:
            self._bytes[byte_index] ^= 1 << bit_index_reversed

    def get_free_item_nums(self, count=1) -> typing.List[int]:
        assert 0 < count < len(self)
        items = []
        for num in range(len(self)):
            if self[num] == 0:
                items.append(num)
                if len(items) == count:
                    return items
        raise MemoryError()

    @classmethod
    def read(
            cls,
            buf: typing.BinaryIO,
            pos: int = None,
            bit_count: int = None,
            size: int = None
    ):
        assert bit_count and not size or size and not bit_count
        tools.seek_if_pos(buf, pos)
        if bit_count:
            assert bit_count % conf.BITS_IN_BYTE == 0
            size = bit_count // conf.BITS_IN_BYTE
        return Bitmap(bytes_=buf.read(size))
