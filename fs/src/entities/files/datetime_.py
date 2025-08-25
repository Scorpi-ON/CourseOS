from datetime import datetime
from typing import BinaryIO, Final

from src import conf, tools
from src.entities.entity import Entity


class Datetime(Entity):
    _STRUCT_FMT: Final = "I"
    SIZE = tools.calcsize(_STRUCT_FMT)
    _DATETIME_FMT: Final = "%d.%m.%y %H:%M"

    @classmethod
    def _get_attrs(cls) -> tuple[str, ...]:
        return ("_datetime",)

    def __init__(self, timestamp: int | None = None) -> None:
        if timestamp is None:
            timestamp = int(datetime.now().timestamp())  # noqa: DTZ005
        assert timestamp < 1 << conf.BITS_IN_BYTE * Datetime.SIZE  # Is timestamp more than 4 bytes
        self._datetime = datetime.fromtimestamp(timestamp)  # noqa: DTZ006

    def write(self, buf: BinaryIO, pos: int | None = None) -> None:
        tools.pack(Datetime._STRUCT_FMT, buf, pos, int(self._datetime.timestamp()))

    @classmethod
    def read(cls, buf: BinaryIO, pos: int | None = None) -> "Datetime":
        value = tools.unpack(Datetime._STRUCT_FMT, buf, pos)[0]
        assert type(value) is int
        return Datetime(value)

    def __str__(self) -> str:
        return self._datetime.strftime(Datetime._DATETIME_FMT)
