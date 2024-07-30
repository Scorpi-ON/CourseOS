import enum

from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidget, QTableWidgetItem, \
    QLineEdit, QPlainTextEdit, QPushButton, QCheckBox
from PyQt6 import uic
from PyQt6.QtCore import Qt

import conf
import tools
from entities.files.inode import Inode
from entities.files.rights import Rights
from entities.main.drive import Drive
from entities.dynamic.file import File


class OpenMode(enum.Enum):
    creation = 0
    edition = 1


class FileDialog(QDialog):
    UI_FILE = 'ui/ui/file_dialog.ui'

    def __init__(
            self,
            parent: QMainWindow,
            title: str,
            drive: Drive,
            file: File = None,
            inode: Inode = None,
            file_content: bytes = None
    ):
        assert file and inode and file_content is not None \
               or not file and not inode and file_content is None
        self.drive = drive
        self.file = file
        self.inode = inode
        self.old_file_content = file_content
        super().__init__(parent)
        self.filenameTxt: QLineEdit | None = None
        self.fileContentTxt: QPlainTextEdit | None = None
        self.propertiesTable: QTableWidget | None = None
        self.suidChb: QCheckBox | None = None
        self.sgidChb: QCheckBox | None = None
        self.rightsTable: QTableWidget | None = None
        self.saveBtn: QPushButton | None = None
        uic.loadUi(FileDialog.UI_FILE, self)
        self.setWindowTitle(title)
        assert None not in (
            self.filenameTxt, self.fileContentTxt, self.propertiesTable,
            self.suidChb, self.sgidChb, self.rightsTable, self.saveBtn
        )
        self.filenameTxt.textEdited.connect(self.saveBtn_enabler)
        if file is None:
            self.open_mode = OpenMode.creation
        else:
            self.fileContentTxt.textChanged.connect(self.saveBtn_enabler)
            self.rightsTable.itemChanged.connect(self.saveBtn_enabler)
            self.suidChb.stateChanged.connect(self.saveBtn_enabler)
            self.sgidChb.stateChanged.connect(self.saveBtn_enabler)
            self.open_mode = OpenMode.edition
            self.fill(file.name, self.inode, file_content)
        self.saveBtn.clicked.connect(self.save)

    @property
    def filename(self) -> str:
        return self.filenameTxt.text().strip()

    @filename.setter
    def filename(self, value: str):
        self.filenameTxt.setText(value.strip())

    @property
    def file_content(self) -> bytes:
        return tools.encode(self.fileContentTxt.toPlainText())

    @file_content.setter
    def file_content(self, value: bytes):
        self.fileContentTxt.setPlainText(tools.decode(value))

    @property
    def rights(self) -> Rights:
        return Rights(
            int(self.suidChb.isChecked()),
            int(self.sgidChb.isChecked()),
            *[self._table_widget_item_to_bit(self.rightsTable.item(i, j))
              for i in range(conf.TRIADE_SIZE)
              for j in range(conf.TRIADE_SIZE)]
        )

    @rights.setter
    def rights(self, value: Rights):
        self.suidChb.setChecked(value.suid == 1)
        self.sgidChb.setChecked(value.sgid == 1)
        for i in range(conf.TRIADE_SIZE):
            for j in range(conf.TRIADE_SIZE):
                self.rightsTable.item(i, j).setCheckState(
                    Qt.CheckState.Checked
                    if value[2 + i * 3 + j] == 1
                    else Qt.CheckState.Unchecked
                )

    def saveBtn_enabler(self):
        if self.open_mode == OpenMode.creation:
            self.saveBtn.setEnabled(bool(self.filename))
        else:
            self.saveBtn.setEnabled(
                self.filename != self.file.name
                or self.file_content != self.old_file_content
                or self.rights != self.inode.rights
            )

    @staticmethod
    def _table_widget_item_to_bit(item: QTableWidgetItem) -> int:
        return 1 if item.checkState() == Qt.CheckState.Checked else 0

    def save(self):
        if self.open_mode == OpenMode.creation:
            self.drive.create_file(self.file_content, self.rights, self.filename)
        else:
            if self.file.name != self.filename:
                self.drive.rename_file(self.file.name, self.filename)
            self.drive.update_file(self.file.inode_num, self.file_content, self.rights)
        self.close()

    def fill(
            self,
            filename: str,
            inode: Inode,
            file_content: bytes
    ):
        current_user_rights = inode.check_rights(self.drive.current_user)
        if current_user_rights[0] == 0:
            self.fileContentTxt.setEnabled(False)
        if current_user_rights[1] == 0:
            self.filenameTxt.setEnabled(False)
            self.fileContentTxt.setEnabled(False)
        self.filename = filename
        self.file_content = file_content
        self.rights = inode.rights
        self.propertiesTable.setEnabled(
            self.drive.current_user.id == inode.user_id
            # or self.drive.current_user.group_id == conf.SYSTEM_USER_AND_GROUP_ID
        )
        for num, prop in enumerate((inode.user_id, inode.group_id, inode.file_size, inode.ctime, inode.mtime)):
            self.propertiesTable.setItem(num, 0, QTableWidgetItem(str(prop)))
        self.propertiesTable.resizeColumnsToContents()
