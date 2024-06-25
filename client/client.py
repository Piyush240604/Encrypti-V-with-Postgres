from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from encrypt import encrypt_file
from register import client_register_user
from login import client_login_user
from gui import EncryptiVGUI
import sys


if __name__ == "__main__":

    # Create an instance of QApplication
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/home/piyush24/Desktop/Encrypti-V-with-Postgres/client/logo.png'))

    # Create an instance of EncryptiVGUI
    window = EncryptiVGUI()

    # Connect login and register buttons to functions
    window.login_button.clicked.connect(lambda: client_login_user(window, window.username_field.text(), window.password_field.text()))
    window.register_button.clicked.connect(lambda: client_register_user(window, window.username_field.text(), window.password_field.text()))

    # Connect encrypt and decrypt buttons to functions
    window.encrypt_file_button.clicked.connect(lambda: encrypt_file(window))

    window.show()
    sys.exit(app.exec())
