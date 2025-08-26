from pathlib import Path

from CourseOS.src.entities.files.datetime_ import Datetime
from CourseOS.src.entities.files.inode import Inode
from CourseOS.src.entities.files.rights import Rights


def test_get_write_size() -> None:
    assert Inode.SIZE == 31


def test_create_write_read() -> None:
    # with pytest.raises(AssertionError):
    #    Inode()
    inode = Inode(Rights(0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1), 2, 3, 2344, Datetime(), Datetime(), [])
    filename = Path("test")
    with filename.open("wb+") as buf:
        inode.write(buf)
        assert buf.tell() == Inode.SIZE
        new_inode = Inode.read(buf, 0)
        assert inode == new_inode
    filename.unlink()
