import base64
from authorize import authorize_user_id
from psycopg2 import sql


def retrieve_keys(db_conn: object, metadata: dict) -> dict:
    try:
        # Establish variables
        file_id: str = metadata["file_id"]
        user_id = authorize_user_id(metadata["username"], metadata["password"])
        print("VARIABLES: ", file_id, user_id)

        # Retrieve file_name, encryption_type, iv and encryption_key from database
        # Establish cursor
        cursor = db_conn.cursor()

        # Write database query
        query = sql.SQL("SELECT file_name, encryption_type, iv, encryption_key FROM FILES WHERE file_id = %s AND user_id = %s")
        cursor.execute(query, (file_id, user_id,))
        result = cursor.fetchone()

        # Close cursor
        cursor.close()

        if result:
            # Convert memoryview objects to bytes if necessary
            file_name, encryption_type, iv, encryption_key = result
            iv = bytes(iv) if isinstance(iv, memoryview) else iv
            encryption_key = bytes(encryption_key) if isinstance(encryption_key, memoryview) else encryption_key
            print(type(result))
            # Prepare result in a JSON serializable format
            result_dict: dict = {
                "file_name": file_name,
                "encryption_type": encryption_type,
                "iv": base64.b64encode(iv).decode('utf-8'),
                "encryption_key": base64.b64encode(encryption_key).decode('utf-8')
            }
            print("RESULT DICTIONARY: ", result_dict)
            return result_dict
        else:
            print("No result found.")
            return None
    
    except Exception as e:
        print("ERROR: ", e)
        return None
