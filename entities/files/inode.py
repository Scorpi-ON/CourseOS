import typing

import conf
import tools
from entities.entity import Entity
from entities.files.datetime_ import Datetime
from entities.files.rights import Rights
from entities.dynamic.user import User


class Inode(Entity):
    _TAIL_STRUCT_FMT = 'BHH' + 'H' * conf.INODE_BLOCK_COUNT
    SIZE = Rights.SIZE + Datetime.SIZE * 2 + tools.calcsize(_TAIL_STRUCT_FMT)

    @classmethod
    def _get_attrs(cls):
        return (
            'rights', 'user_id', 'group_id', 'file_size', 'ctime', 'mtime', 'address_array'
        )

    def __init__(
            self,
            rights: Rights,
            user_id: int,
            group_id: int,
            file_size: int,
            ctime: Datetime,
            mtime: Datetime,
            address_array: typing.List[int]
    ):
        assert len(address_array) <= conf.INODE_BLOCK_COUNT
        self.rights = rights
        self.user_id = user_id
        self.group_id = group_id
        self.file_size = file_size
        self.ctime = ctime
        self.mtime = mtime
        self._address_array = address_array

    @property
    def address_array(self) -> typing.List[int]:
        empty_address_count = conf.INODE_BLOCK_COUNT - len(self._address_array)
        return [*self._address_array, *(0,) * empty_address_count]

    @address_array.setter
    def address_array(self, value: typing.List[int]):
        self._address_array = value

    def write(self, buf, pos=None):
        self.rights.write(buf, pos)
        self.ctime.write(buf)
        self.mtime.write(buf)
        tools.pack(
            Inode._TAIL_STRUCT_FMT,
            buf,
            None,
            self.user_id,
            self.group_id,
            self.file_size,
            *self.address_array
        )

    @classmethod
    def read(cls, buf, pos=None):
        rights = Rights.read(buf, pos)
        ctime = Datetime.read(buf)
        mtime = Datetime.read(buf)
        user_id, group_id, file_size, *address_array = tools.unpack(Inode._TAIL_STRUCT_FMT, buf)
        return Inode(
            rights,
            user_id,
            group_id,
            file_size,
            ctime,
            mtime,
            list(address_array)
        )

    def check_rights(self, user: User | None) -> typing.Tuple[int, int, int] | None:
        if user is None or self.group_id != user.group_id and user.group_id == conf.SYSTEM_USER_AND_GROUP_ID:
            return 1, 1, 1
        elif self.user_id == conf.SYSTEM_USER_AND_GROUP_ID:
            return
        elif self.user_id == user.id:
            return self.rights.user_read, self.rights.user_write, self.rights.user_execute
        elif self.group_id == user.group_id:
            return self.rights.others_read, self.rights.others_write, self.rights.others_execute
        else:
            return self.rights.others_read, self.rights.others_write, self.rights.others_execute
