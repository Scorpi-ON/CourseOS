from pathlib import Path

from src.entities.files.rights import Rights


def test_size() -> None:
    assert Rights.SIZE == 2


def test_create_write_read() -> None:
    rights = Rights(0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0)
    filename = Path("test")
    with filename.open("wb") as buf:
        rights.write(buf)
        assert buf.tell() == Rights.SIZE
    with filename.open("rb") as buf:
        new_rights = Rights.read(buf)
        assert new_rights.suid == 0
        assert rights == new_rights
    filename.unlink()
