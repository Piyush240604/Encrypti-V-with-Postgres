from authorize import authorize_user_id
from encryption.permission import get_access_type
from encryption.date_time import get_datetime
from encryption.file_encryption import store_file
from encryption.folder_encryption import check_folder_path, store_folder
from encryption.parent_folder_id import get_parent_folder_id
import uuid
import os.path


class Store_Metadata:

    def __init__(self, db_conn, metadata: dict):
        
        # User Variables
        self.username: str = metadata["username"]
        self.password: str = metadata["password"]
        self.user_id: str = authorize_user_id(self.username, self.password)

        # Folder Variables
        self.folder_path = metadata["file_directory"]
        self.folder_id: bytes = uuid.uuid4()
        self.access_type = get_access_type(file_path=self.folder_path)
        self.parent_folder_id = get_parent_folder_id(db_conn, os.path.dirname(self.folder_path)) if metadata["parent_folder"] == 1 else None
        
        ''' parent_folder_path is the path of the parent directory to keep track of folders inside folders'''

        # --File Variables--
        self.file_id = uuid.uuid4()
        self.file_name: str = metadata["original_file_name"]
        self.encryption_type: str = metadata["encryption_type"]
        self.date_encrypted = get_datetime()
        self.iv: bytes = bytes.fromhex(metadata["iv"])
        self.encryption_key: bytes = bytes.fromhex(metadata["key_bytes"])

# Receive all the information from Client and store into the database
def store_encryption_key_client(db_conn: object, received_metadata: dict):

    # Initialize class and store all the metadata
    storage: object = Store_Metadata(db_conn, metadata=received_metadata)

    # check if file path already exists
    prexisting_folder_id = check_folder_path(db_conn=db_conn, metadata=storage)

    # if folder_id already exists in the database and encryption type is folder, then dont do folder insertion
    if storage.encryption_type == "folder" and prexisting_folder_id is not None:
        storage.folder_id = prexisting_folder_id
    elif prexisting_folder_id is None or storage.encryption_type == "file":
        folder_result = store_folder(db_conn=db_conn, metadata=storage)
    
    
    # Store file metadata in files table if folder metadata storage was successful
    file_result: bool = store_file(db_conn=db_conn, metadata=storage)
    
    # Return file_id
    return storage.file_id