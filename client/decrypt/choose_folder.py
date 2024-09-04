from PyQt5.QtWidgets import QMessageBox
from decrypt.decrypt import perform_decryption
import os
import uuid

def collect_file_info(window: object, file: str):
    try:
        # open the file
        with open(file, 'rb') as f:
            # Read the file
            cipher: bytes = f.read()

            # Get file_id
            file_id = str(uuid.UUID(bytes=cipher[:16]))
            # Get encrypted_file_bytes
            encrypted_file_bytes = cipher[16:]

        return file_id, encrypted_file_bytes
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Error occurred while decrypting: {str(e)}")
        return None

def list_folder_items(window: object, directory: str, parent_folder: int, files: list, file_ids: list, encrypted_file_bytes_list: list):
    # List all files in the directory
    directory_items: list = os.listdir(directory)
    length_directory_items = len(directory_items)
    flag = 0 # In case, people try to decrypt folder that is not encrypted only

    # Checks if the folder has any files or folders
    if directory_items == []:
        # If the folder is the main directory
        if parent_folder == 0:
            window.show_message("No Files or Folders in this Directory!")
        return
    
    # Loop through all the items and collect their file ids and encrypted file bytes
    for item in directory_items:
        
        # Get full path of item
        item = os.path.join(directory, item)

        # Check if item is file
        if os.path.isfile(item):
            # Check if the item is a V file, continue if it is
            if item.split('.')[1] != 'V':
                flag += 1
                continue
            
            # Get file information
            file_id, encrypted_file_bytes = collect_file_info(window, item)
            
            # Append to the list
            file_ids.append(file_id)
            encrypted_file_bytes_list.append(encrypted_file_bytes)
            files.append(item)
        else:
            # Set parent folder to 1
            parent_folder = 1
            # Recursively call the function
            list_folder_items(window, item, parent_folder, files, file_ids, encrypted_file_bytes_list)
    
    # Flag them fools
    if flag == length_directory_items:
        window.show_message("This folder is not Encrypted! Choose a different Folder.")
        return
    
    return files, file_ids, encrypted_file_bytes_list

    
def choose_folder_decryption(window: object):
    # Choose folder to decrypt
    selected_folder = window.pick_directory()

    # Check if folder is selected
    if selected_folder == '':
        window.show_message("No Folder Selected!")
        return
    
    # Establish a parents_folder variable
    parent_folder: int = 0

    # Establish variables to be read
    file_ids: list = []
    encrypted_file_bytes_list: list = []
    files: list = []
    
    
    files, file_ids, encrypted_file_bytes_list = list_folder_items(window, selected_folder, parent_folder, files, file_ids, encrypted_file_bytes_list)

    # Send the files and file information to perform decryption
    perform_decryption(window, files, file_ids, encrypted_file_bytes_list)


