# encrypt.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
import os
import random
import string
import requests

# Function to generate a random encryption key
def generate_random_key():
    return get_random_bytes(32)

# Function to generate a random file name
def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to encrypt bytes using AES-GCM
def encrypt_bytes(bytes, key):
    cipher = AES.new(key, AES.MODE_GCM)
    encrypted_bytes, tag = cipher.encrypt_and_digest(pad(bytes, AES.block_size))
    return encrypted_bytes, cipher.nonce

# Function to send metadata to slave server
def send_keys(file_id, file_directory, original_file_name, key_bytes, iv, username, password):
    url = "http://localhost:5001/file_encryption_client"

    headers = {
        "Content-Type": "application/json"
    }
    
    # Form message
    encrypt_data = {
        "file_id": file_id.hex(),
        "file_directory": file_directory,
        "original_file_name": original_file_name,
        "key_bytes": key_bytes.hex(),
        "iv": iv.hex(),
        "username": username,
        "password": password
    }

    # Send details to the server and receive confirmation
    response = requests.post(url, json=encrypt_data, headers=headers)


def write(window, fileName, selectedDir, selectedFile, cipher):
    with open(os.path.join(selectedDir, fileName + ".V"), "wb") as file:
        file.write(cipher)

    os.remove(selectedFile) # Deletes the file that was not encrypted
    window.show_message("File encrypted successfully.")


def perform_encryption(window, selected_file, encrypt_dialog, create_new_name, username, password):
    encrypt_dialog.destroy()
    try:
        # Gets the directory of the selected file if the value of save_in_new_location is 0, otherwise executes pick_dir function to get new location directory
        selected_dir = os.path.dirname(selected_file)

        # Get name of the file along with extension
        original_file_name = os.path.basename(selected_file)

        # Generate a file ID to store for the database
        file_id = generate_random_key()

        # Get the directory path of the file
        file_directory = os.path.dirname(selected_file)

        # Split the extension from the file name if create_new_name value is 0, otherwise generate a random name, and attach to file_name variable
        file_name = os.path.splitext(original_file_name)[0] if not create_new_name else generate_random_filename()

        # Generate key_bytes to be used for encryption
        key_bytes = generate_random_key()

        # Open the file to read and encrypt its contents with encrypt_bytes function
        with open(selected_file, "rb") as file:
            file_bytes = file.read()
        encrypted_file_bytes, iv = encrypt_bytes(file_bytes, key_bytes)

        # Store cipher as encrypted file_id + encrypted content
        cipher = file_id + encrypted_file_bytes

        # Create a message containing data to send to server
        send_keys(file_id.hex(), file_directory, original_file_name, key_bytes.hex(), iv.hex(), username, password)
        
        # Create file with .V extension in the provided directory to write and write the cipher onto it
        write(window, file_name, selected_dir, selected_file, cipher)

    except Exception as e:
        print(e)
        window.show_message("Error encrypting file.")


# Choose file to Encrypt
def encrypt_file(window):
    
    # Open Window to select file
    selected_file, _ = window.pick_file()

    # If file has been selected
    if selected_file:

        # Open window and show encryption options
        encrypt_dialog = QDialog(window)
        encrypt_dialog.setWindowTitle("Encryption Options")
        encrypt_dialog.setGeometry(100, 100, 300, 150)

        create_new_name = QCheckBox("Change File Name", encrypt_dialog)

        encrypt_button = QPushButton("Encrypt", encrypt_dialog)
        encrypt_button.clicked.connect(lambda: perform_encryption(window, selected_file, encrypt_dialog, create_new_name.isChecked(), window.usernameField.text(), window.passwordField.text()))

        cancelButton = QPushButton("Cancel", encrypt_dialog)
        cancelButton.clicked.connect(encrypt_dialog.reject)

        create_new_name.move(10, 10)
        encrypt_button.move(50, 80)
        cancelButton.move(160, 80)

        encrypt_dialog.exec()
    
    else:
        window.show_message("No File selected!")