import os

from src.tools import calcsize, pack, unpack


def test_calcsize():
    assert calcsize('>I') == 4
    assert calcsize('H') == 2
    assert calcsize('B') == 1


def test_pack_unpack():
    filename = 'test'
    fmt = 'IHB'
    size = 4 + 2 + 1
    assert calcsize(fmt) == size
    with open(filename, 'wb') as buf:
        pack(fmt, buf, 0, 1, 2, 3)
        assert buf.tell() == size
    with open(filename, 'rb') as buf:
        assert unpack(fmt, buf) == (1, 2, 3)
        assert buf.tell() == size
    os.remove(filename)
