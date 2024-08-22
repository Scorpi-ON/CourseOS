from src import conf, tools
from src.entities.main.drive import Drive
from src.entities.main.superblock import Superblock
from src.entities.files.bitmap import Bitmap


def test_create_file():
    content = tools.encode('1' * conf.BLOCK_SIZE * conf.INODE_BLOCK_COUNT)
    superblock = Superblock(
        conf.FS_TYPE,
        conf.BLOCK_SIZE,
        conf.INODE_COUNT,
        conf.BLOCK_COUNT,
        conf.FREE_INODE_COUNT,
        conf.FREE_BLOCK_COUNT
    )
    with open(conf.DRIVE_FILENAME, 'wb+') as buf:
        drive = Drive(
            buf,
            superblock,
            Bitmap(superblock.inode_count),
            Bitmap(superblock.block_count)
        )
        drive.write()
        drive.create_file(content, filename='Тест')
        new_drive = Drive.read(buf)
        assert drive == new_drive
        assert content == drive.read_file(3)[1]
