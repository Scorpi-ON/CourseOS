import os

from entities.files.inode import Inode
from entities.files.rights import Rights
from entities.files.bitmap import Bitmap
from entities.files.datetime_ import Datetime


def test_get_write_size():
    assert Inode.SIZE == 31


def test_create_write_read():
    # with pytest.raises(AssertionError):
    #    Inode()
    inode = Inode(Rights(0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1), 2, 3, 2344, Datetime(), Datetime(), [])
    filename = 'test'
    with open(filename, 'wb+') as buf:
        inode.write(buf)
        assert buf.tell() == Inode.SIZE
        new_inode = Inode.read(buf, 0)
        assert inode == new_inode
    os.remove(filename)
