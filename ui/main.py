from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, \
    QListWidget, QListWidgetItem, QMessageBox, QPushButton
from PyQt6 import uic

import conf
from ui.file_dialog import FileDialog
from ui.add_group_or_user_dialog import AddGroupOrUserWindow, AdditionMode
from entities.main.drive import Drive


class MainWindow(QMainWindow):
    UI_FILE = 'ui/ui/main.ui'

    def __init__(self, drive: Drive):
        super().__init__()
        self.drive = drive
        self.groupTable: QTableWidget | None = None
        self.userTable: QTableWidget | None = None
        self.addGroupBtn: QPushButton | None = None
        self.addUserBtn: QPushButton | None = None
        self.fileList: QListWidget | None = None
        self.createFileBtn: QPushButton | None = None
        self.deleteSelectedBtn: QPushButton | None = None
        self.copyBtn: QPushButton | None = None
        uic.loadUi(MainWindow.UI_FILE, self)
        assert None not in (
            self.fileList, self.groupTable, self.userTable, self.addGroupBtn,
            self.addUserBtn, self.createFileBtn, self.deleteSelectedBtn, self.copyBtn
        )
        self.setWindowTitle(f'{self.drive.current_user.login}@PythOS')
        self.load_groups()
        self.load_users()
        self.load_files()

        if self.drive.current_user.group_id == conf.SYSTEM_USER_AND_GROUP_ID:
            self.addGroupBtn.clicked.connect(self.add_group)
            self.addUserBtn.clicked.connect(self.add_user)
        else:
            self.addGroupBtn.setEnabled(False)
            self.addUserBtn.setEnabled(False)
        self.groupTable.itemDoubleClicked.connect(self.edit_group)
        self.userTable.itemDoubleClicked.connect(self.edit_user)
        self.fileList.itemSelectionChanged.connect(self.btn_enabler)
        self.fileList.itemDoubleClicked.connect(self.open_selected_file)
        self.createFileBtn.clicked.connect(self.create_file)
        self.deleteSelectedBtn.clicked.connect(self.delete_selected)
        self.copyBtn.clicked.connect(self.copy_file)

    def copy_file(self):
        try:
            file = self.drive.get_file_by_name(self.fileList.selectedItems()[0].text())
            inode, content = self.drive.read_file(file.inode_num)
            filename = file.name
            ext, _, filename = filename.rpartition('.')
            filename += ' — копия'
            if ext:
                filename += f'.{ext}'
            self.drive.create_file(
                content,
                inode.rights,
                filename
            )
        except Exception as exception:
            QMessageBox(
                QMessageBox.Icon.Critical,
                'Ошибка копирования файла',
                str(exception),
                QMessageBox.StandardButton.Ok,
                self
            ).show()
        else:
            self.load_files()

    def btn_enabler(self):
        is_selected = bool(self.fileList.selectedIndexes())
        self.deleteSelectedBtn.setEnabled(is_selected)
        self.copyBtn.setEnabled(is_selected)

    def load_files(self):
        self.fileList.clear()
        for file in self.drive.root:
            self.fileList.addItem(file.name)

    def load_groups(self):
        self.groupTable.clearContents()
        for num, group in enumerate(self.drive.groups):
            self.groupTable.insertRow(num)
            self.groupTable.setItem(num, 0, QTableWidgetItem(str(group.id)))
            self.groupTable.setItem(num, 1, QTableWidgetItem(group.name))

    def load_users(self):
        self.userTable.clearContents()
        for num, user in enumerate(self.drive.users):
            self.userTable.insertRow(num)
            self.userTable.setItem(num, 0, QTableWidgetItem(str(user.id)))
            self.userTable.setItem(num, 1, QTableWidgetItem(str(user.group_id)))
            self.userTable.setItem(num, 2, QTableWidgetItem(user.login))

    def edit_group(self):
        row = self.groupTable.selectedItems()[0].row()
        if row == 0 or self.drive.current_user.group_id != conf.SYSTEM_USER_AND_GROUP_ID:
            return
        AddGroupOrUserWindow(
            self,
            self.drive,
            AdditionMode.group,
            *[
                self.groupTable.item(row, i)
                for i in range(self.groupTable.columnCount())
            ]
        ).exec()
        self.load_groups()

    def edit_user(self):
        row = self.userTable.selectedItems()[0].row()
        if row == 0 or self.drive.current_user.group_id != conf.SYSTEM_USER_AND_GROUP_ID:
            return
        AddGroupOrUserWindow(
            self,
            self.drive,
            AdditionMode.user,
            *[
                self.userTable.item(row, i)
                for i in range(self.userTable.columnCount())
            ]
        ).exec()
        self.load_users()

    def add_group(self):
        AddGroupOrUserWindow(self, self.drive, AdditionMode.group).exec()
        self.load_groups()

    def add_user(self):
        AddGroupOrUserWindow(self, self.drive, AdditionMode.user).exec()
        self.load_users()

    def open_selected_file(self, item: QListWidgetItem):
        file_to_open = item.text()
        file = self.drive.get_file_by_name(file_to_open)
        try:
            inode, file_content = self.drive.read_file(file.inode_num)
            FileDialog(self, file.name, self.drive, file, inode, file_content).exec()
        except Exception as exception:
            QMessageBox(
                QMessageBox.Icon.Critical,
                'Ошибка работы с файлом',
                str(exception),
                QMessageBox.StandardButton.Ok,
                self
            ).show()
        else:
            self.load_files()

    def create_file(self):
        try:
            FileDialog(self, 'Новый файл', self.drive).exec()
        except Exception as exception:
            QMessageBox(
                QMessageBox.Icon.Critical,
                'Ошибка создания файла',
                str(exception),
                QMessageBox.StandardButton.Ok,
                self
            ).show()
        else:
            self.load_files()

    def delete_selected(self):
        filename_to_delete = self.fileList.selectedItems()[0].text()
        button = QMessageBox(
            QMessageBox.Icon.Question,
            'Удаление файла',
            f'Вы действительно хотите удалить файл "{filename_to_delete}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            self
        ).exec()
        if button == QMessageBox.StandardButton.Yes:
            try:
                self.drive.delete_file(self.drive.get_file_by_name(filename_to_delete).inode_num)
            except Exception as exception:
                QMessageBox(
                    QMessageBox.Icon.Critical,
                    'Ошибка удаления файла',
                    str(exception),
                    QMessageBox.StandardButton.Ok,
                    self
                ).show()
            else:
                self.load_files()
