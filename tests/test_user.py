import os

import pytest

import conf
from entities.users.user import User


def test_size():
    login = 'Неизвестен'
    user = User(login=login)
    assert user.size == 3 + len(login) + conf.HASH_SIZE


def test_create_write_read():
    # with pytest.raises(AssertionError):
    #     Group(id_=-1)
    #     Group(name='')
    user = User()
    filename = 'test'
    with open(filename, 'wb') as buf:
        user.write(buf)
        assert buf.tell() == user.size
    with open(filename, 'rb') as buf:
        new_user = User.read(buf)
        assert user == new_user
    os.remove(filename)
