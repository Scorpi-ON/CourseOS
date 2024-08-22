from src.entities.dynamic.user import User


def test_create_write_read():
    user = User(0, 'Test user', 'passwd')
    assert user == User.from_bytes(bytes(user))[0]
