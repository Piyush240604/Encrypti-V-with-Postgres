from authorize import authorize_user_id
from permission import get_access_type
from date_time import get_datetime
import uuid


# Store metadata in file and folder table
def store_encryption_key_client(db_conn, data):

    # Get user-id
    username = data.get('username')
    password = data.get('password')
    user_id = authorize_user_id(username, password)

    # Establish variables
    # --Folder Variables--
    folder_id = str(uuid.uuid4())
    folder_path = data.get('file_directory')
    access_type = get_access_type(folder_path)
    parent_folder_id = None

    # --File Variables--
    file_id = str(uuid.uuid4())
    file_name = data.get('original_file_name')
    date_encrypted = get_datetime()
    iv = data.get('iv')

    # --COMPLETE THE PROGRAM--
    

