import conf
import tools
from entities.entity import Entity
from entities.files.block import Block


class Superblock(Entity):
    _TAIL_STRUCT_FMT = 'H' * 5

    @classmethod
    def _get_attrs(cls):
        return (
            'fs_type', 'block_size', 'block_count', 'inode_count',
            'free_block_count', 'free_inode_count'
        )

    @property
    def _struct_fmt(self):                                               # First extra byte is needed
        return f'{1 + len(self.fs_type)}p{Superblock._TAIL_STRUCT_FMT}'  # for the string length

    @property
    def size(self):
        return tools.calcsize(self._struct_fmt)

    def __init__(
            self,
            fs_type: str,
            block_size: int,
            inode_count: int,
            block_count: int,
            free_inode_count: int,
            free_block_count: int
    ):
        assert (
            1 <= len(fs_type) <= conf.MAX_BYTE_VALUE
            and inode_count % conf.BITS_IN_BYTE == 0
            and block_count % conf.BITS_IN_BYTE == 0
        )
        self.fs_type = fs_type
        self.block_size = block_size
        Block.size = block_size
        self.inode_count = inode_count
        self.block_count = block_count
        self.free_inode_count = free_inode_count
        self.free_block_count = free_block_count

    def write(self, buf, pos=None):
        tools.pack(
            self._struct_fmt,
            buf,
            pos,
            tools.encode(self.fs_type),
            self.block_size,
            self.inode_count,
            self.block_count,
            self.free_inode_count,
            self.free_block_count
        )

    @classmethod
    def read(cls, buf, pos=None):
        tools.seek_if_pos(buf, pos)
        fs_type_size = tools.unpack('B', buf)[0]
        fs_type = tools.decode(buf.read(fs_type_size))
        block_size, inode_count, block_count, free_inode_count, free_block_count \
            = tools.unpack(Superblock._TAIL_STRUCT_FMT, buf)
        return Superblock(
            fs_type,
            block_size,
            inode_count,
            block_count,
            free_inode_count,
            free_block_count
        )
