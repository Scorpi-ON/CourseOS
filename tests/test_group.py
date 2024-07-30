import os

import pytest

from entities.users.group import Group


def test_size():
    name = 'Неопределённые личности'
    group = Group(255, name)
    assert group.size == 2 + len(name)


def test_create_write_read():
    with pytest.raises(AssertionError):
        Group(id_=-1)
        Group(name='')
    group = Group()
    filename = 'test'
    with open(filename, 'wb') as buf:
        group.write(buf)
        assert buf.tell() == group.size
    with open(filename, 'rb') as buf:
        new_group = Group.read(buf)
        assert group == new_group
    os.remove(filename)
