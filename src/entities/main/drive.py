import typing
import enum
import math
from functools import cached_property

from src import conf, tools
from src.entities.entity import Entity
from src.entities.main.superblock import Superblock
from src.entities.dynamic.file import File
from src.entities.dynamic.user import User
from src.entities.dynamic.group import Group
from src.entities.files.inode import Inode
from src.entities.files.bitmap import Bitmap
from src.entities.files.rights import Rights
from src.entities.files.datetime_ import Datetime


class ReservedInodeNum(enum.Enum):
    groups = 0
    root = 2
    users = 1


class Drive(Entity):
    @classmethod
    def _get_attrs(cls):
        return (
            'superblock', 'inode_bitmap', 'block_bitmap', 'inode_pos', 'block_pos',
            'groups', 'users', 'root', 'current_user'
        )

    def __init__(
            self,
            buf: typing.BinaryIO,
            superblock: Superblock,
            inode_bitmap: Bitmap,
            block_bitmap: Bitmap
    ):
        assert (
            not buf.closed and buf.mode in ('rb+', 'wb')
            and superblock.inode_count == len(inode_bitmap)
            and superblock.block_count == len(block_bitmap)
        )
        self.buf = buf
        self.superblock = superblock
        self.inode_bitmap = inode_bitmap
        self.block_bitmap = block_bitmap
        self.groups = [
            Group(conf.SYSTEM_GROUP_NAME)
        ]
        self.users = [
            User(
                conf.SYSTEM_USER_AND_GROUP_ID,
                conf.ADMIN_LOGIN,
                password_hash=conf.ADMIN_PASSWORD_HASH
            )
        ]
        self.root = [
            File(reserved_inode_num.value, f'.{reserved_inode_num.name}')
            for reserved_inode_num in ReservedInodeNum
        ]
        self.current_user: User | None = None

    @cached_property
    def inode_pos(self):
        return self.superblock.size + self.inode_bitmap.size + self.block_bitmap.size

    @cached_property
    def block_pos(self):
        return self.inode_pos + Inode.SIZE * self.superblock.inode_count

    @cached_property
    def size(self):
        return self.block_pos + self.superblock.block_size * self.superblock.block_count

    def get_file_by_name(self, filename: str) -> File | None:
        for file in self.root:
            if file.name == filename:
                return file

    def write(self, pos=0):
        self.superblock.write(self.buf, pos)                     # Writing superblock
        self.buf.write(bytes(self.size - self.superblock.size))  # and filling the rest of disk space with zeros
        self.create_file(Group.to_bytes(self.groups))
        self.create_file(User.to_bytes(self.users))
        self.create_file(File.to_bytes(self.root))

    @classmethod
    def read(cls, buf, pos=0):
        superblock = Superblock.read(buf, pos)
        drive = Drive(
            buf,
            superblock,
            inode_bitmap=Bitmap.read(buf, bit_count=superblock.inode_count),
            block_bitmap=Bitmap.read(buf, bit_count=superblock.block_count)
        )
        drive.groups = Group.from_bytes(
            drive.read_file(ReservedInodeNum.groups.value)[1]
        )
        drive.users = User.from_bytes(
            drive.read_file(ReservedInodeNum.users.value)[1]
        )
        drive.root = File.from_bytes(
            drive.read_file(ReservedInodeNum.root.value)[1]
        )
        return drive

    def _get_block_count(self, size: int) -> int:
        block_count = math.ceil(size / self.superblock.block_size)
        if size == 0 or block_count >= conf.INODE_BLOCK_COUNT:
            block_count += 1
        return block_count

    def _get_and_check_block_count_difference(self, size: int, current_block_count=0) -> int:
        block_count = self._get_block_count(size)
        block_count_difference = block_count - current_block_count
        if block_count_difference > self.superblock.free_block_count:
            raise MemoryError('Недостаточно места на диске')
        if block_count_difference > conf.BLOCK_COUNT_TO_STORE_FILE_OF_MAX_SIZE:
            raise MemoryError('Превышен максимально допустимый размер файла')
        return block_count_difference

    def _save_updated_superblock_and_bitmaps(self):
        self.superblock.write(self.buf, 0)
        self.inode_bitmap.write(self.buf)
        self.block_bitmap.write(self.buf)

    def _write_to_blocks(
            self,
            address_array: typing.List[int],
            content: bytes
    ):
        indirect_addressing_block_address = 0
        if len(address_array) > conf.INODE_BLOCK_COUNT:
            indirect_addressing_block_address = address_array.pop(conf.INDIRECT_ADDRESSING_BLOCK_NUM)
        for num, address in enumerate(address_array):
            indirect_num = num - conf.INDIRECT_ADDRESSING_BLOCK_NUM
            if indirect_num >= 0:
                tools.pack(
                    conf.BLOCK_ADDRESS_FMT,
                    self.buf,
                    self.block_pos + indirect_addressing_block_address
                    + conf.BLOCK_ADDRESS_SIZE * indirect_num,
                    address
                )
            content_offset = self.superblock.block_size * num
            self.buf.seek(self.block_pos + address)
            self.buf.write(content[content_offset:content_offset + self.superblock.block_size])

    def create_file(
            self,
            content: bytes,
            rights=Rights(),
            filename: str = None
    ):
        if filename is not None:
            filename = filename.strip()
            if not filename:
                raise ValueError('Имя файла не должно быть пустым или заполненным пробелами')
            if self.get_file_by_name(filename) is not None:
                raise SystemError(f'Файл с именем "{filename}" уже существует')
        inode_num = self.inode_bitmap.get_free_item_nums()[0]
        block_count = self._get_and_check_block_count_difference(len(content))
        block_nums = self.block_bitmap.get_free_item_nums(block_count)
        address_array = [self.superblock.block_size * num for num in block_nums]
        current_datetime = Datetime()
        inode = Inode(
            rights=rights,
            user_id=self.current_user.id if self.current_user else conf.SYSTEM_USER_AND_GROUP_ID,
            group_id=self.current_user.group_id if self.current_user else conf.SYSTEM_USER_AND_GROUP_ID,
            file_size=len(content),
            ctime=current_datetime,
            mtime=current_datetime,
            address_array=address_array[:conf.INODE_BLOCK_COUNT]
        )

        self.superblock.free_inode_count -= 1
        self.inode_bitmap[inode_num] = 1
        self.superblock.free_block_count -= len(block_nums)
        for num in block_nums:
            self.block_bitmap[num] = 1
        self._save_updated_superblock_and_bitmaps()

        inode.write(self.buf, self.inode_pos + Inode.SIZE * inode_num)
        self._write_to_blocks(address_array, content)

        if filename:
            self.root.append(File(inode_num, filename))
            self.root.sort(key=lambda file: file.name)
            user = self.current_user
            self.current_user = None
            self.update_file(ReservedInodeNum.root.value, File.to_bytes(self.root))
            self.current_user = user

    def read_file(self, inode_num: int) -> typing.Tuple[Inode, bytearray]:
        inode = Inode.read(self.buf, self.inode_pos + Inode.SIZE * inode_num)
        content = bytearray()
        current_user_rights = inode.check_rights(self.current_user)
        if not current_user_rights:
            raise SystemError('Файл является системным и не доступен для чтения.')
        elif current_user_rights[0] == 0 or inode.file_size == 0:
            return inode, content
        block_count = self._get_block_count(inode.file_size)
        file_tail_size = inode.file_size % self.superblock.block_size
        for num in range(conf.INDIRECT_ADDRESSING_BLOCK_NUM):
            self.buf.seek(self.block_pos + inode.address_array[num])
            if num < block_count - 1:
                content.extend(self.buf.read(self.superblock.block_size))
            else:
                content.extend(self.buf.read(file_tail_size))
                break
        indirect_block_count = block_count - conf.INODE_BLOCK_COUNT
        if indirect_block_count > 0:
            indirect_addressing_block_address = inode.address_array[conf.INDIRECT_ADDRESSING_BLOCK_NUM]
            indirect_address_array = tools.unpack(
                conf.BLOCK_ADDRESS_FMT * indirect_block_count,
                self.buf,
                self.block_pos + indirect_addressing_block_address
            )
            for num in range(indirect_block_count):
                self.buf.seek(self.block_pos + indirect_address_array[num])
                content.extend(self.buf.read(
                    self.superblock.block_size
                    if num < indirect_block_count - 1 or file_tail_size == 0
                    else file_tail_size
                ))
        return inode, content

    def update_file(
            self,
            inode_num: int,
            new_content: bytes = None,
            rights: Rights = None
    ):
        inode = Inode.read(self.buf, self.inode_pos + Inode.SIZE * inode_num)
        # inode.check_rights(self.current_user)
        if not new_content:
            assert rights is not None
        else:
            old_block_count = self._get_block_count(inode.file_size)
            address_array = inode.address_array[:old_block_count]
            indirect_block_count = old_block_count - conf.INODE_BLOCK_COUNT
            if indirect_block_count > 0:
                indirect_addressing_block_address = address_array[conf.INDIRECT_ADDRESSING_BLOCK_NUM]
                indirect_address_array = tools.unpack(
                    conf.BLOCK_ADDRESS_FMT * indirect_block_count,
                    self.buf,
                    self.block_pos + indirect_addressing_block_address
                )
                address_array.extend(indirect_address_array)
            block_count_difference = self._get_and_check_block_count_difference(len(new_content), old_block_count)
            if block_count_difference > 0:
                new_block_nums = self.block_bitmap.get_free_item_nums(block_count_difference)
                for num in new_block_nums:
                    self.block_bitmap[num] = 1
                    address_array.append(self.superblock.block_size * num)
            elif block_count_difference < 0:
                for _ in range(block_count_difference * -1):
                    self.block_bitmap[address_array.pop() // self.superblock.block_size] = 0
            inode.file_size = len(new_content)
            inode.address_array = address_array[:conf.INODE_BLOCK_COUNT]
            self._write_to_blocks(address_array, new_content)
        inode.mtime = Datetime()
        if rights:
            inode.rights = rights
        self._save_updated_superblock_and_bitmaps()
        inode.write(self.buf, self.inode_pos + Inode.SIZE * inode_num)
        Inode.read(self.buf, self.inode_pos + Inode.SIZE * inode_num)

    def rename_file(self, old_name: str, new_name: str):
        # inode.check_rights(self.current_user)
        file = self.get_file_by_name(old_name)
        file.name = new_name
        self.root.sort(key=lambda file_: file_.name)
        user = self.current_user
        self.current_user = None
        self.update_file(ReservedInodeNum.root.value, File.to_bytes(self.root))
        self.current_user = user

    def delete_file(self, inode_num: int):
        inode = Inode.read(self.buf, self.inode_pos + Inode.SIZE * inode_num)
        current_user_rights = inode.check_rights(self.current_user)
        if not current_user_rights:
            raise SystemError('Файл является системным и не подлежит удалению.')
        elif current_user_rights[1] == 0:
            raise SystemError('Вы не имеете права на удаление этого файла.')
        block_count = self._get_block_count(inode.file_size)
        indirect_block_count = block_count - conf.INODE_BLOCK_COUNT
        address_array = inode.address_array[:block_count]
        if indirect_block_count >= 0:
            indirect_addressing_block_address = address_array[conf.INDIRECT_ADDRESSING_BLOCK_NUM]
            address_array.extend(
                tools.unpack(
                    conf.BLOCK_ADDRESS_FMT * indirect_block_count,
                    self.buf,
                    self.block_pos + indirect_addressing_block_address
                )
            )

        self.superblock.free_inode_count += 1
        self.inode_bitmap[inode_num] = 0
        self.superblock.free_block_count += block_count
        for address in address_array:
            self.block_bitmap[address // self.superblock.block_size] = 0
        self._save_updated_superblock_and_bitmaps()
        for num, file in enumerate(self.root):
            if file.inode_num == inode_num:
                self.root.pop(num)
                break
        self.update_file(ReservedInodeNum.root.value, File.to_bytes(self.root))
