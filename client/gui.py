from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QGuiApplication, QMovie

class EncryptiVGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Encrypti V")
        screen_res = QGuiApplication.primaryScreen().availableGeometry().size()
        self.setGeometry(screen_res.width() // 2 - 200, screen_res.height() // 2 - 125, 400, 250)
        self.setFixedSize(400, 250)

        self.set_background()
        self.create_labels()
        self.create_buttons()
        self.hide_components(1)

    def set_background(self):
        self.background_label = QLabel(self)
        self.movie = QMovie(r"assets\background.gif")
        self.movie.setSpeed(25)
        self.background_label.setMovie(self.movie)
        self.movie.start()
        self.background_label.setGeometry(0, 0, 700, 350)
        self.background_label.lower()

    def create_labels(self):
        self.welcome_label = self.create_label("Welcome to Encrypti V", 90, 30, 250, 20, 16)
        self.username_label = self.create_label("Username:", 50, 80, 80, 20)
        self.password_label = self.create_label("Password:", 50, 120, 80, 20)

    def create_label(self, text, x, y, width, height, font_size=None):
        label = QLabel(text, self)
        label.setGeometry(x, y, width, height)
        if font_size:
            label.setStyleSheet(f"font-size: {font_size}pt; color: white; font-weight: bold;")
        else:
            label.setStyleSheet("color: white; font-weight: bold;")
        return label

    def create_buttons(self):
        # Username and Password Field
        self.username_field = self.create_text_field(140, 80, 200, 25)
        self.password_field = self.create_text_field(140, 120, 200, 25, True)
        
        # Login and Register Button
        self.login_button = self.create_button("Login", 140, 160, 90, 30)
        self.register_button = self.create_button("Register", 250, 160, 90, 30)

        self.encrypt_file_button = self.create_button("Encrypt File", 100, 110, 90, 30)
        self.decrypt_file_button = self.create_button("Decrypt File", 100, 150, 90, 30)

        # Encrypt Folder and Decrypt Folder Button
        self.encrypt_folder_button = self.create_button("Encrypt Folder", 210, 110, 90, 30)
        self.decrypt_folder_button = self.create_button("Decrypt Folder", 210, 150, 90, 30)

    def create_text_field(self, x, y, width, height, password=False):
        field = QLineEdit(self)
        field.setGeometry(x, y, width, height)
        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    def create_button(self, text, x, y, width, height):
        button = QPushButton(text, self)
        button.setGeometry(x, y, width, height)
        return button

    def hide_components(self, button_id):
        if button_id == 1:
            for widget in [self.encrypt_file_button, self.decrypt_file_button, self.encrypt_folder_button, self.decrypt_folder_button]:
                widget.hide()
        elif button_id == 2:
            widgets_to_hide = [
                self.username_label, self.username_field,
                self.password_label, self.password_field,
                self.login_button, self.register_button, self.welcome_label
            ]
            for widget in widgets_to_hide:
                widget.hide()

    def show_message(self, message):
        QMessageBox.information(self, "Message", message)

    def show_buttons(self):
        for widget in [self.encrypt_file_button, self.decrypt_file_button, self.encrypt_folder_button, self.decrypt_folder_button]:
            widget.show()

    def pick_file(self):
        return QFileDialog.getOpenFileName(self, "Pick a file")

    def pick_directory(self):
        return QFileDialog.getExistingDirectory(self, "Pick a directory")

