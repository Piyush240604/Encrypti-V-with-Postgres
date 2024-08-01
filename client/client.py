# GUI Libraries
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import EncryptiVGUI

# Login and Registration imports
from authentication.register import client_register_user
from authentication.login import client_login_user

# Encryption Imports
from encrypt.choose_file import choose_file_encryption
from encrypt.choose_folder import choose_folder_encryption

# Decryption Imports
from decrypt.choose_file import choose_file_decryption

import sys


if __name__ == "__main__":

    # Create an instance of QApplication
    app: object = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets\logo.png'))

    # Create an instance of EncryptiVGUI
    window: object = EncryptiVGUI()

    # Connect login and register buttons to functions
    # FUTURE EDIT: Make it such that its able to stores user_id thus, reducing the amount of parameters in encrypt.py
    window.login_button.clicked.connect(lambda: client_login_user(window))
    window.register_button.clicked.connect(lambda: client_register_user(window))

    # Connect encrypt and decrypt buttons to functions --> FILE
    window.encrypt_file_button.clicked.connect(lambda: choose_file_encryption(window))
    window.decrypt_file_button.clicked.connect(lambda: choose_file_decryption(window))

    # Connect encrypt and decrypt buttons to functions --> FOLDER
    window.encrypt_folder_button.clicked.connect(lambda: choose_folder_encryption(window))

    window.show()
    sys.exit(app.exec())

