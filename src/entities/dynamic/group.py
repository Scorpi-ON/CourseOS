from src import conf, tools
from src.entities.dynamic.dynamic_entity import DynamicEntity


class Group(DynamicEntity):
    ADMIN_ID = conf.SYSTEM_USER_AND_GROUP_ID
    id = ADMIN_ID

    @classmethod
    def _get_attrs(cls):
        return 'id', 'name'

    def __init__(
            self,
            name: str
    ):
        self.id = Group.id
        Group.id += 1
        self.name = name

    def __bytes__(self):
        return tools.encode(f'{self.id} {self.name}')

    @classmethod
    def from_bytes(cls, bytes_):
        lines = tools.decode(bytes_).splitlines()
        groups = []
        for line in lines:
            id_, _, name = line.partition(' ')
            if int(id_) == Group.ADMIN_ID:
                Group.id = Group.ADMIN_ID
            groups.append(Group(name))
        return groups
