from pathlib import Path

import pytest

from src.entities.files.bitmap import Bitmap


def test_create_write_read() -> None:
    with pytest.raises(AssertionError):
        Bitmap(bit_count=3)
    with pytest.raises(AssertionError):
        Bitmap(bits=bytes(5))
    with pytest.raises(AssertionError):
        Bitmap(bits=bytes([2, 1, 0, 0, 1, 0, 1, 0]))
    bitmap = Bitmap(bits=bytes([1, 1, 0, 0, 1, 0, 1, 0]))
    filename = Path("test")
    with filename.open("wb") as buf:
        bitmap.write(buf)
        assert buf.tell() == 1
    with filename.open("rb") as buf:
        new_bitmap = Bitmap.read(buf, 0, 8)
        assert bitmap == new_bitmap
    filename.unlink()


def test_bit_edition() -> None:
    bitmap = Bitmap(bits=bytes([1, 1, 1, 1, 1, 1, 1, 1]))
    bitmap[1] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
    bitmap[1] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
    bitmap[4] = 0
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 0, 1, 1, 1]))
    bitmap[4] = 1
    assert bitmap == Bitmap(bits=bytes([1, 0, 1, 1, 1, 1, 1, 1]))
