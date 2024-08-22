import os

from src.entities.files.rights import Rights


def test_size():
    assert Rights.SIZE == 2


def test_create_write_read():
    rights = Rights(0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0)
    filename = 'test'
    with open(filename, 'wb') as buf:
        rights.write(buf)
        assert buf.tell() == Rights.SIZE
    with open(filename, 'rb') as buf:
        new_rights = Rights.read(buf)
        assert new_rights.suid == 0
        assert rights == new_rights
    os.remove(filename)
