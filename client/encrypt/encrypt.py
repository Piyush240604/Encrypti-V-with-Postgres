# encrypt.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from encrypt.send_keys import send_keys
import os
import random
import string
import uuid

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

def write(fileName, selectedDir, selectedFile, cipher) -> str:

    # Open the file in write mode and write the cipher text
    with open(os.path.join(selectedDir, fileName + ".V"), "wb") as file:
        file.write(cipher)

    os.remove(selectedFile) # Deletes the file that was not encrypted
    return True

def perform_encryption(window, selected_file, create_new_name, encryption_type, parent_folder):
    try:
        
        # Get username and password
        username = window.username_field.text()
        password = window.password_field.text()

        # Gets the directory of the selected file
        selected_dir = os.path.dirname(selected_file)

        # Get name of the file along with extension
        original_file_name = os.path.basename(selected_file)

        # Split the extension from the file name if create_new_name value is 0, otherwise generate a random name, and attach to file_name variable
        file_name = os.path.splitext(original_file_name)[0] if not create_new_name else generate_random_filename()

        # Generate key_bytes to be used for encryption
        key_bytes = generate_random_key()

        # Open the file to read and encrypt its contents with encrypt_bytes function
        with open(selected_file, "rb") as file:
            file_bytes = file.read()
        encrypted_file_bytes, iv = encrypt_bytes(file_bytes, key_bytes)

        # Create a message containing data to send to server
        # Form message
        encryption_metadata = {
            "file_directory": selected_dir,
            "original_file_name": original_file_name,
            "key_bytes": key_bytes.hex(),
            "iv": iv.hex(),
            "username": username,
            "password": password,
            "encryption_type": encryption_type,
            "parent_folder": parent_folder
        }
        
        # Send the message to server and receive file_id
        file_id_str: str = send_keys(encryption_metadata)

        # Check for any errors
        if file_id_str == "E":
            window.show_message("Error in Encryption [SERVER SIDE ERROR]")
            return
        
        # Convert file_id to bytes so it can be used by cipher
        file_id = uuid.UUID(file_id_str).bytes
        
        print("FILE ID: ", file_id, "TYPE: ", type(file_id))

        # Create a cipher
        cipher = file_id + encrypted_file_bytes

        # Create file with .V extension in the provided directory to write and write the cipher onto it
        write_result = write(file_name, selected_dir, selected_file, cipher)

        if encryption_type == "file":
            window.show_message("File encrypted successfully.")

    except Exception as e:
        print(e)
        window.show_message("Error encrypting file.")

# RETURN FILE ID FROM SLAVE SERVER TO CLIENT AND LET CLIENT WRITE THE FILE ID ONTO THE ENCRYPTED FILE!