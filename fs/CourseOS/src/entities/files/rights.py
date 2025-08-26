import enum
from typing import BinaryIO, Literal

from CourseOS.src import conf, tools
from CourseOS.src.entities.entity import Entity
from CourseOS.src.entities.files.bitmap import Bitmap


class RightsIndex(enum.Enum):
    suid = 0
    sgid = 1
    user_read = 2
    user_write = 3
    user_execute = 4
    group_read = 5
    group_write = 6
    group_execute = 7
    others_read = 8
    others_write = 9
    others_execute = 10


class Rights(Entity):
    _STRUCT_FMT = "H"
    SIZE = tools.calcsize(_STRUCT_FMT)

    @classmethod
    def _get_attrs(cls) -> tuple[str, ...]:
        return ("_bitmap",)

    def __init__(
        self,
        suid: Literal[0, 1] = 0,
        sgid: Literal[0, 1] = 0,
        user_read: Literal[0, 1] = 0,
        user_write: Literal[0, 1] = 0,
        user_execute: Literal[0, 1] = 0,
        group_read: Literal[0, 1] = 0,
        group_write: Literal[0, 1] = 0,
        group_execute: Literal[0, 1] = 0,
        others_read: Literal[0, 1] = 0,
        others_write: Literal[0, 1] = 0,
        others_execute: Literal[0, 1] = 0,
        bitmap: Bitmap | None = None,
    ) -> None:
        if bitmap is None:
            self._bitmap = Bitmap(
                bits=bytes(
                    (
                        suid,
                        sgid,
                        user_read,
                        user_write,
                        user_execute,
                        group_read,
                        group_write,
                        group_execute,
                        others_read,
                        others_write,
                        others_execute,
                        *(0 for _ in range(conf.BITS_IN_BYTE * Rights.SIZE - len(RightsIndex))),
                    )
                )
            )
        else:
            self._bitmap = bitmap

    def __getitem__(self, num: int) -> Literal[0, 1]:
        assert 0 <= num < len(RightsIndex)
        return self._bitmap[num]

    def __getattr__(self, item: str) -> int:
        return self._bitmap[RightsIndex[item].value]

    def __setattr__(self, key: str, value: int) -> None:
        if key == "_bitmap":
            super().__setattr__(key, value)
        else:
            self._bitmap[RightsIndex[key].value] = value

    def write(self, buf: BinaryIO, pos: int | None = None) -> None:
        tools.seek_if_pos(buf, pos)
        self._bitmap.write(buf)

    @classmethod
    def read(cls, buf: BinaryIO, pos: int | None = None) -> "Rights":
        tools.seek_if_pos(buf, pos)
        return Rights(bitmap=Bitmap.read(buf, size=Rights.SIZE))
