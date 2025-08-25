from src import tools
from src.entities.dynamic.dynamic_entity import DynamicEntity


class File(DynamicEntity):
    @classmethod
    def _get_attrs(cls) -> tuple[str, ...]:
        return "inode_num", "name"

    def __init__(self, inode_num: int, name: str) -> None:
        self.inode_num = inode_num
        self.name = name

    def __bytes__(self) -> bytes:
        return tools.encode(f"{self.inode_num} {self.name}")

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> list["File"]:
        lines = tools.decode(bytes_).splitlines()
        files = []
        for line in lines:
            inode_num, _, name = line.partition(" ")
            files.append(File(int(inode_num), name))
        return files
