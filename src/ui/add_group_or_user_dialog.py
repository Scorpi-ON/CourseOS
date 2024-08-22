import enum

from PyQt6.QtWidgets import QMainWindow, QDialog, QLineEdit, QPushButton, QComboBox, QStackedWidget, QMessageBox, \
    QTableWidgetItem
from PyQt6 import uic

from src import conf
from src.entities.main.drive import Drive, ReservedInodeNum
from src.entities.dynamic.group import Group
from src.entities.dynamic.user import User
from src.entities.dynamic.file import File


class AdditionMode(enum.Enum):
    group = 0
    user = 1


class AddGroupOrUserWindow(QDialog):
    UI_FILE = 'src/ui/ui/add_group_or_user_dialog.ui'

    def __init__(
            self,
            parent: QMainWindow,
            drive: Drive,
            addition_mode: AdditionMode,
            *items: QTableWidgetItem
    ):
        super().__init__(parent)
        self.drive = drive
        self.group_id: int | None = None
        self.user_id: int | None = None
        self.addition_mode = addition_mode
        self.stackedWidget: QStackedWidget | None = None
        self.groupNameTxt: QLineEdit | None = None
        self.groupCbx: QComboBox | None = None
        self.loginTxt: QLineEdit | None = None
        self.passwordTxt: QLineEdit | None = None
        self.addBtn: QPushButton | None = None
        uic.loadUi(AddGroupOrUserWindow.UI_FILE, self)
        assert None not in (
            self.stackedWidget, self.groupNameTxt,
            self.loginTxt, self.groupCbx, self.passwordTxt, self.addBtn
        )
        self.stackedWidget.setCurrentIndex(self.addition_mode.value)
        if self.addition_mode == AdditionMode.user:
            assert not items or len(items) == 3
            group_id = None
            if items:
                user_id, group_id, login = items
                self.user_id = int(user_id.text())
                self.loginTxt.setText(login.text())
            for group in self.drive.groups[conf.SYSTEM_USER_AND_GROUP_ID + 1:]:
                self.groupCbx.addItem(group.name, group.id)
                if group_id and group.id == int(group_id.text()):
                    self.groupCbx.setCurrentText(group.name)
            self.groupCbx.currentIndexChanged.connect(self.addBtn_enabler)
            self.loginTxt.textChanged.connect(self.addBtn_enabler)
            self.passwordTxt.textChanged.connect(self.addBtn_enabler)
        else:
            assert not items or len(items) == 2
            if items:
                group_id, group_name = items
                self.groupNameTxt.setText(group_name.text())
                self.group_id = int(group_id.text())
            self.groupNameTxt.textChanged.connect(
                lambda new_text: self.addBtn.setEnabled(bool(new_text))
            )
        self.addBtn.clicked.connect(self.save)

    @property
    def login(self) -> str:
        return self.loginTxt.text().strip()

    @property
    def password(self) -> str:
        return self.passwordTxt.text()

    def save(self):
        if self.addition_mode == AdditionMode.user:
            if self.user_id is None:
                for user in self.drive.users:
                    if user.login == self.login:
                        QMessageBox(
                            QMessageBox.Icon.Critical,
                            'Ошибка добавления пользователя',
                            f'Пользователь «{self.login}» уже существует. Введите другой логин..',
                            QMessageBox.StandardButton.Ok,
                            self
                        ).exec()
                        return
                self.drive.users.append(User(
                    self.groupCbx.currentData(),
                    self.login,
                    self.password
                ))
            else:
                for user in self.drive.users:
                    if user.id == self.user_id:
                        user.group_id = self.groupCbx.currentData()
                        user.login = self.login
                        user.set_password(self.password)
                        break
            self.drive.update_file(ReservedInodeNum.users.value, File.to_bytes(self.drive.users))
        else:
            group_name = self.groupNameTxt.text().strip()
            if self.group_id is None:
                for group in self.drive.groups:
                    if group.name == group_name:
                        QMessageBox(
                            QMessageBox.Icon.Critical,
                            'Ошибка добавления группы',
                            f'Группа «{group_name}» уже существует. Введите другое название.',
                            QMessageBox.StandardButton.Ok,
                            self
                        ).exec()
                        return
                self.drive.groups.append(Group(group_name))
            else:
                for group in self.drive.groups:
                    if group.id == self.group_id:
                        group.name = group_name
                        break
            self.drive.update_file(ReservedInodeNum.groups.value, File.to_bytes(self.drive.groups))
        self.close()

    def addBtn_enabler(self):
        self.addBtn.setEnabled(
            bool(self.login)
            and self.groupCbx.currentIndex() != -1
            and bool(self.password)
        )
