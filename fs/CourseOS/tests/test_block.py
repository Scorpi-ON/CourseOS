from pathlib import Path

from CourseOS.src.conf import BLOCK_SIZE
from CourseOS.src.entities.files.block import Block


def test_create_write_read() -> None:
    block = Block(bytes_=bytes(range(BLOCK_SIZE)))
    filename = Path("test")
    with filename.open("wb") as buf:
        block.write(buf)
        assert buf.tell() == BLOCK_SIZE
    with filename.open("rb") as buf:
        new_block = Block.read(buf)
        assert block == new_block
    filename.unlink()
