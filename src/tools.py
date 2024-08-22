import struct
import typing
import hashlib

from . import conf


def encode(string: str) -> bytes:
    return string.encode(conf.WIN_1251)


def decode(bytes_: bytes) -> str:
    return bytes_.decode(conf.WIN_1251)


def hash_password(password: str) -> str:
    return hashlib.sha256(encode(password)).hexdigest()


def _correct_fmt(fmt: str):
    if not fmt.startswith('>'):
        fmt = f'>{fmt}'
    return fmt


def calcsize(fmt: str) -> int:
    fmt = _correct_fmt(fmt)
    return struct.calcsize(fmt)


def seek_if_pos(
        buf: typing.BinaryIO,
        pos: int | None
):
    if pos is not None:
        buf.seek(pos)


def pack(fmt: str, buf: typing.BinaryIO, pos=None, *args):
    seek_if_pos(buf, pos)
    fmt = _correct_fmt(fmt)
    buf.write(struct.pack(fmt, *args))


def unpack(fmt: str, buf: typing.BinaryIO, pos=None) -> typing.Tuple[typing.Any, ...]:
    fmt = _correct_fmt(fmt)
    seek_if_pos(buf, pos)
    return struct.unpack(fmt, buf.read(calcsize(fmt)))
