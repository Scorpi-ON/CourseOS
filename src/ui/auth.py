import typing

from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton
from PyQt6 import uic, QtGui, QtCore

from src import conf, tools
from src.entities.main.drive import Drive
from src.ui.main import MainWindow


class AuthWindow(QMainWindow):
    UI_FILE = 'src/ui/ui/auth.ui'

    def __init__(self, drive: Drive):
        super().__init__()
        self.drive = drive
        self.main_window: MainWindow | None = None
        self.loginTxt: QLineEdit | None = None
        self.passwordTxt: QLineEdit | None = None
        self.confirmBtn: QPushButton | None = None
        uic.loadUi(AuthWindow.UI_FILE, self)
        assert None not in (self.loginTxt, self.passwordTxt, self.confirmBtn)
        self.confirmBtn.clicked.connect(self.confirm)

    def auth_error(self, error):
        self.loginTxt.clear()
        self.passwordTxt.clear()
        self.statusBar().showMessage(f'Не удалось войти: {error}')

    def confirm(self):
        login = self.loginTxt.text()
        password = self.passwordTxt.text()
        for user in self.drive.users:
            if user.id != conf.SYSTEM_USER_AND_GROUP_ID and user.login == login:
                expected_password_hash = user.password_hash
                break
        else:
            self.auth_error('неверный логин')
            return
        if expected_password_hash == tools.hash_password(password):
            self.hide()
            self.drive.current_user = user
            self.main_window = MainWindow(self.drive)
            self.main_window.show()
        else:
            self.auth_error('неверный пароль')

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == int(QtCore.Qt.Key.Key_Enter) - 1:  # No idea, why -1, but otherwise
            self.confirmBtn.click()                          # it isn't recognized as Enter

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]):
        a0.accept()
        self.destroy()
