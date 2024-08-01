from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from decrypt.delete_keys import delete_record
from decrypt.get_keys import get_file_metadata
import uuid
import os

# Function to decrypt bytes using AES-GCM
def decrypt_bytes(encryptedText, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    try:
        decryptedBytes = unpad(cipher.decrypt(encryptedText), AES.block_size)
        return decryptedBytes
    except (ValueError, KeyError):
        return None

# Decrypt the file
def perform_decryption(window, file, file_id_bytes, encrypted_file_bytes):
    try:
        # Convert file_id_bytes to UUID
        file_id: uuid = uuid.UUID(bytes=file_id_bytes)

        # Get details of metadata of the file
        decryption_metadata: dict= get_file_metadata(window, file_id)

        # Establish variables
        iv = decryption_metadata["iv"]
        encryption_key = decryption_metadata["encryption_key"]

        # Get decrypted_bytes
        decrypted_bytes = decrypt_bytes(encrypted_file_bytes, encryption_key, iv)

        if decrypted_bytes is not None:
            
            # Make the file
            decrypted_file = os.path.join(os.path.dirname(file), decryption_metadata["file_name"])

            # Open the file to write and write the contents produced by decryption
            with open(decrypted_file, "wb") as d_file:
                d_file.write(decrypted_bytes)
            os.remove(file) # Remove selected file

            # Delete Record
            if delete_record(window, file_id):
                window.show_message("File Decrypted Successfully!")
            else:
                window.show_message("Error Decrypting File!")

        
    
    except Exception as e:
        print(e)
        window.show_message("Error Decrypting File!")