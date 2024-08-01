from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
from encrypt.encrypt import perform_encryption
import os

# Function to loop through all the files in the directories
def list_files_in_directory(window, directory, new_name, parent_folder) -> int:
    
    
    # Get a list of the directory
    directory_items: list = os.listdir(directory)

    # Checks if the folder has any files or folders
    if directory_items == []:
        # If the folder is the main directory
        if parent_folder == 0:
            window.show_message("No Files or Folders in this Directory!")
        return
    
    # Establish encryption type
    encryption_type: str = "folder"
    
    # Encryption and flag counter
    encryption_count: int = 0
    '''flag: int = 0'''

    print("DIRECTORY ITEMS:", directory_items)
    print("---------------------")
    # Loop through each item in the directory
    for item in directory_items:
        
        ''' 
        FEATURE TO BE ADDED PROBABLY 
        # Check if the file has a V extension
        if os.path.splitext(item)[1] == ".V":
            print(item, "Already encrypted!")
            flag = 1
            continue
        '''
        print("Encryption Count:", encryption_count)

        # Get full path of file and store it as file
        item = os.path.join(directory, item)
        
        # Check if the item is a file
        if os.path.isfile(item):
            perform_encryption(window, item, new_name, encryption_type, parent_folder)
            encryption_count += 1
        
        # The item is a folder
        else:
            # Set parent_folder to 1
            parent_folder = 1

            # Recursively call the function
            list_files_in_directory(window, item, new_name, parent_folder)
    
    return encryption_count
    

def handle_destruction_and_encryption(window, selected_folder, new_name, encrypt_dialog):

    # DESTROY ENCRYPT_DIALOG
    encrypt_dialog.destroy()

    # Initialize parent_folder
    parent_folder: int = 0

    # Initiate folder encryption
    encryption_count = list_files_in_directory(window, selected_folder, new_name, parent_folder)
    
    # Check if you were fooled!
    
    '''if encryption_count == 0 and flag == 1:
        window.show_message("These Files are already Encrypted!")'''
    if encryption_count == 0:
        window.show_message("No Files in the Folder to Encrypt!")
    else:
        window.show_message("Encryption Successful!")
        
# Function to choose encrypt folder
def choose_folder_encryption(window):

    # Open window to select directory
    selected_folder = window.pick_directory()
    print(selected_folder)

    # If no folder is selected
    if selected_folder == '':
        window.show_message("No Folder Selected!")
        return

    # Open window and show encryption options
    encrypt_dialog = QDialog(window)
    encrypt_dialog.setWindowTitle("Encryption Options")
    encrypt_dialog.setGeometry(100, 100, 300, 150)

    create_new_name = QCheckBox("Change File Name", encrypt_dialog)

    encrypt_button = QPushButton("Encrypt", encrypt_dialog)
    encrypt_button.clicked.connect(lambda: handle_destruction_and_encryption(window, selected_folder, create_new_name.isChecked(), encrypt_dialog))

    cancelButton = QPushButton("Cancel", encrypt_dialog)
    cancelButton.clicked.connect(encrypt_dialog.reject)

    create_new_name.move(10, 10)
    encrypt_button.move(50, 80)
    cancelButton.move(160, 80)

    encrypt_dialog.exec()
    
