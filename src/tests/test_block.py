import os

from src.conf import BLOCK_SIZE
from src.entities.files.block import Block


def test_create_write_read():
    block = Block(bytes_=bytes(range(BLOCK_SIZE)))
    filename = 'test'
    with open(filename, 'wb') as buf:
        block.write(buf)
        assert buf.tell() == BLOCK_SIZE
    with open(filename, 'rb') as buf:
        new_block = Block.read(buf)
        assert block == new_block
    os.remove(filename)
