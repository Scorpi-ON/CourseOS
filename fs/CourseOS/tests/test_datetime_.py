from pathlib import Path

import pytest

from CourseOS.src.entities.files.datetime_ import Datetime


def test_size() -> None:
    assert Datetime.SIZE == 4


def test_create_write_read() -> None:
    with pytest.raises(AssertionError):
        Datetime(1 << 32)
    datetime = Datetime()
    filename = Path("test")
    with filename.open("wb") as buf:
        datetime.write(buf)
        assert buf.tell() == Datetime.SIZE
    with filename.open("rb") as buf:
        new_datetime = Datetime.read(buf)
        assert datetime == new_datetime
    filename.unlink()
