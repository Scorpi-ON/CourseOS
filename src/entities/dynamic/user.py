from src import conf, tools
from src.entities.dynamic.dynamic_entity import DynamicEntity


class User(DynamicEntity):
    ADMIN_ID = conf.SYSTEM_USER_AND_GROUP_ID + 1
    id = ADMIN_ID

    @classmethod
    def _get_attrs(cls):
        return 'id', 'group_id', 'login', 'password_hash'

    def __init__(
            self,
            group_id: int,
            login: str,
            password: str = None,
            password_hash: str = None
    ):
        assert password and not password_hash or password_hash and not password
        self.id = User.id
        User.id += 1
        self.group_id = group_id
        self.login = login
        if password:
            self.set_password(password)
        else:
            self.password_hash = password_hash

    def __bytes__(self):
        return tools.encode(f'{self.id} {self.group_id} {self.login} {self.password_hash}')

    @classmethod
    def from_bytes(cls, bytes_):
        lines = tools.decode(bytes_).splitlines()
        users = []
        for line in lines:
            data, _, password_hash = line.rpartition(' ')
            id_, group_id, login = data.split(' ', 2)
            if int(id_) == User.ADMIN_ID:
                User.id = User.ADMIN_ID
            users.append(
                User(int(group_id), login, password_hash=password_hash)
            )
        return users

    def set_password(self, password: str):
        self.password_hash = tools.hash_password(password)
