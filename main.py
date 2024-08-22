import os
import sys

from PyQt6.QtWidgets import QApplication

from src import conf
from src.ui.auth import AuthWindow
from src.entities.main.drive import Drive
from src.entities.main.superblock import Superblock
from src.entities.files.bitmap import Bitmap


if __name__ == '__main__':
    os.chdir(sys.path[0])
    if not os.path.exists(conf.DRIVE_FILENAME):
        with open(conf.DRIVE_FILENAME, 'wb') as buf:
            superblock = Superblock(
                conf.FS_TYPE,
                conf.BLOCK_SIZE,
                conf.INODE_COUNT,
                conf.BLOCK_COUNT,
                conf.FREE_INODE_COUNT,
                conf.FREE_BLOCK_COUNT
            )
            drive = Drive(
                buf,
                superblock,
                Bitmap(superblock.inode_count),
                Bitmap(superblock.block_count)
            )
            drive.write()
    app = QApplication([])
    with open(conf.DRIVE_FILENAME, 'rb+') as buf:
        drive = Drive.read(buf)
        auth_window = AuthWindow(drive)
        while auth_window.isHidden():
            auth_window.show()
            app.exec()
