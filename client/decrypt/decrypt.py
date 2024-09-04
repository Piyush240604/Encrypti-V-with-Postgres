from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from decrypt.delete_keys import delete_record
from decrypt.get_keys import get_file_metadata
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
def perform_decryption(window, files: list, file_ids: list, encrypted_file_bytes_list: list):
    try:
        # Get details of metadata of the file
        decryption_metadata: dict = get_file_metadata(window, file_ids)
        
        # Check if metadata was properly received
        if decryption_metadata == {}:
            window.show_message("Error Decrypting File")
            print("No Metadata was received!")
            return 

        # Establish variables
        file_name: list = decryption_metadata["file_name"]
        iv: list = decryption_metadata["iv"]
        encryption_key: list = decryption_metadata["encryption_key"]
        count: int = len(decryption_metadata["file_name"])

        for i in range(count):
            # Get decrypted_bytes
            decrypted_bytes = decrypt_bytes(encrypted_file_bytes_list[i], encryption_key[i], iv[i])
                
            # Make the file
            decrypted_file = os.path.join(os.path.dirname(files[i]), file_name[i])

            # Open the file to write and write the contents produced by decryption
            with open(decrypted_file, "wb") as d_file:
                d_file.write(decrypted_bytes)
            os.remove(files[i]) # Remove selected file

        # Delete Record
        if delete_record(window, file_ids):
            window.show_message("Decryption Successfull!")
    
    except Exception as e:
        print(e)
        window.show_message("Error Decrypting File!")