import os

from entities.main.superblock import Superblock


def test_create_write_read():
    # with pytest.raises(AssertionError):
    #     Superblock('not_fs')
    superblock = Superblock()
    filename = 'test'
    with open(filename, 'wb') as buf:
        superblock.write(buf)
        assert buf.tell() == superblock.size
    with open(filename, 'rb') as buf:
        new_superblock = Superblock.read(buf)
        assert superblock == new_superblock
    os.remove(filename)
