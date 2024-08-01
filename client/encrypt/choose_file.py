from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
from encrypt.encrypt import perform_encryption

# Make a function specifically for handling destruction of encrypt dialog and call perform encryption
def handle_destruction_and_encryption(window, selected_file, encrypt_dialog, new_name):

    # DESTROY THE ENCRYPT DIALOG
    encrypt_dialog.destroy()

    # Set encryption type
    encryption_type: str = "file"

    # Call encrypt function
    perform_encryption(window, selected_file, new_name, encryption_type, parent_folder=0)

# Choose file to Encrypt
def choose_file_encryption(window):
    
    # Open Window to select file
    selected_file, _ = window.pick_file()

    # If file has not been selected
    if selected_file == "":
        window.show_message("No File selected!")

    # If file is selected
    # Open window and show encryption options
    encrypt_dialog = QDialog(window)
    encrypt_dialog.setWindowTitle("Encryption Options")
    encrypt_dialog.setGeometry(100, 100, 300, 150)

    create_new_name = QCheckBox("Change File Name", encrypt_dialog)

    encrypt_button = QPushButton("Encrypt", encrypt_dialog)
    encrypt_button.clicked.connect(lambda: handle_destruction_and_encryption(window, selected_file, encrypt_dialog, create_new_name.isChecked()))

    cancelButton = QPushButton("Cancel", encrypt_dialog)
    cancelButton.clicked.connect(encrypt_dialog.reject)

    create_new_name.move(10, 10)
    encrypt_button.move(50, 80)
    cancelButton.move(160, 80)

    encrypt_dialog.exec()