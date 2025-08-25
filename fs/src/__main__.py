import os
import sys

from PyQt6.QtWidgets import QApplication

from src import conf
from src.entities.files.bitmap import Bitmap
from src.entities.main.drive import Drive
from src.entities.main.superblock import Superblock
from src.ui.auth import AuthWindow

if __name__ == "__main__":
    os.chdir(sys.path[0])
    if not conf.DRIVE_FILENAME.exists():
        with conf.DRIVE_FILENAME.open("wb") as buf:
            superblock = Superblock(
                conf.FS_TYPE,
                conf.BLOCK_SIZE,
                conf.INODE_COUNT,
                conf.BLOCK_COUNT,
                conf.FREE_INODE_COUNT,
                conf.FREE_BLOCK_COUNT,
            )
            drive = Drive(buf, superblock, Bitmap(superblock.inode_count), Bitmap(superblock.block_count))
            drive.write()
    app = QApplication([])
    with conf.DRIVE_FILENAME.open("rb+") as buf:
        drive = Drive.read(buf)
        auth_window = AuthWindow(drive)
        auth_window.show()
        app.exec()
