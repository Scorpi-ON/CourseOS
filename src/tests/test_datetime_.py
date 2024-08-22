import os

import pytest

from src.entities.files.datetime_ import Datetime


def test_size():
    assert Datetime.SIZE == 4


def test_create_write_read():
    with pytest.raises(AssertionError):
        Datetime(1 << 32)
    datetime = Datetime()
    filename = 'test'
    with open(filename, 'wb') as buf:
        datetime.write(buf)
        assert buf.tell() == Datetime.SIZE
    with open(filename, 'rb') as buf:
        new_datetime = Datetime.read(buf)
        assert datetime == new_datetime
    os.remove(filename)
