from PyQt5.QtWidgets import QMessageBox
from decrypt.decrypt import perform_decryption

# Choose file to decrypt
def choose_file_decryption(window):
    
    # Select file
    select_file, _ = window.pick_file()

    if select_file:
        try:
            with open(select_file, "rb") as file:
                cipher: bytes = file.read()
            
            # send cipher for decryption
            perform_decryption(window=window, file=select_file, file_id_bytes=cipher[:16], encrypted_file_bytes=cipher[16:])

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Error occurred while decrypting: {str(e)}")