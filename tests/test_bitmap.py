import os

import pytest

from entities.files.bitmap import Bitmap


def test_create_write_read():
    with pytest.raises(AssertionError):
        Bitmap(bit_count=3)
        Bitmap(bits=bytes(5))
    with pytest.raises(ValueError):
        Bitmap(bits=bytes([2, 1, 0, 0, 1, 0, 1, 0]))
    bitmap = Bitmap(bits=bytes([1, 1, 0, 0, 1, 0, 1, 0]))
    filename = 'test'
    with open(filename, 'wb') as buf:
        bitmap.write(buf)
        assert buf.tell() == 1
    with open(filename, 'rb') as buf:
        new_bitmap = Bitmap.read(buf, 8)
        assert bitmap == new_bitmap
    os.remove(filename)


def test_bit_edition():
    bitmap = Bitmap(bits=bytes([1, 1, 1, 1, 1, 1, 1, 1]))
    bitmap[1] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
    bitmap[1] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
    bitmap[4] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 0, 1, 1, 1]))
    bitmap[4] = 1
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
