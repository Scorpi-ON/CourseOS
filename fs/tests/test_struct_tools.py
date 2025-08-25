from pathlib import Path

from src.tools import calcsize, pack, unpack


def test_calcsize() -> None:
    assert calcsize(">I") == 4
    assert calcsize("H") == 2
    assert calcsize("B") == 1


def test_pack_unpack() -> None:
    filename = Path("test")
    fmt = "IHB"
    size = 4 + 2 + 1
    assert calcsize(fmt) == size
    with filename.open("wb") as buf:
        pack(fmt, buf, 0, 1, 2, 3)
        assert buf.tell() == size
    with filename.open("rb") as buf:
        assert unpack(fmt, buf) == (1, 2, 3)
        assert buf.tell() == size
    filename.unlink()
