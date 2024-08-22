from datetime import datetime

from src import conf, tools
from src.entities.entity import Entity


class Datetime(Entity):
    _STRUCT_FMT = 'I'
    SIZE = tools.calcsize(_STRUCT_FMT)
    _DATETIME_FMT = '%d.%m.%y %H:%M'

    @classmethod
    def _get_attrs(cls):
        return ('_datetime',)

    def __init__(
            self,
            timestamp: int = None
    ):
        if timestamp is None:
            timestamp = int(datetime.now().timestamp())
        assert timestamp < 1 << conf.BITS_IN_BYTE * Datetime.SIZE  # Is timestamp more than 4 bytes
        self._datetime = datetime.fromtimestamp(timestamp)

    def write(self, buf, pos=None):
        tools.pack(
            Datetime._STRUCT_FMT,
            buf,
            pos,
            int(self._datetime.timestamp())
        )

    @classmethod
    def read(cls, buf, pos=None):
        return Datetime(
            tools.unpack(Datetime._STRUCT_FMT, buf, pos)[0]
        )

    def __str__(self):
        return self._datetime.strftime(Datetime._DATETIME_FMT)
