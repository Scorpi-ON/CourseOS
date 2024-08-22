import pytest

from src.entities.dynamic.group import Group


def test_create_write_read():
    group = Group('Тестовая группа ')
    assert group == Group.from_bytes(bytes(group))[0]
