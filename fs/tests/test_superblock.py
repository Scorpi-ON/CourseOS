from pathlib import Path

from src import conf
from src.entities.main.superblock import Superblock


def test_create_write_read() -> None:
    superblock = Superblock(
        conf.FS_TYPE, conf.BLOCK_SIZE, conf.INODE_COUNT, conf.BLOCK_COUNT, conf.FREE_INODE_COUNT, conf.FREE_BLOCK_COUNT
    )
    filename = Path("test")
    with filename.open("wb") as buf:
        superblock.write(buf)
        assert buf.tell() == superblock.size
    with filename.open("rb") as buf:
        new_superblock = Superblock.read(buf)
        assert superblock == new_superblock
    filename.unlink()
