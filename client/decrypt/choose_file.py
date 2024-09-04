from PyQt5.QtWidgets import QMessageBox
from decrypt.decrypt import perform_decryption
import uuid

# Choose file to decrypt
def choose_file_decryption(window):
    
    # Select file
    select_file, _ = window.pick_file()

    if select_file:
        try:
            with open(select_file, "rb") as file:
                cipher: bytes = file.read()
            
            # Make a list to store file_id and encrypted_file_bytes
            file_ids: list = [str(uuid.UUID(bytes=cipher[:16]))]
            encrypted_file_bytes_list: list = [cipher[16:]]
            files: list = [select_file]

            # send cipher for decryption
            perform_decryption(window, files, file_ids, encrypted_file_bytes_list)

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Error occurred while decrypting: {str(e)}")