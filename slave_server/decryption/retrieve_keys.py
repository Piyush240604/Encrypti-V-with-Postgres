import base64
from authorize import authorize_user_id
from psycopg2 import sql


def retrieve_keys(db_conn: object, metadata: dict) -> dict:
    try:
        # Prepare the resultant metadata structure
        result_dict: dict = {
            "file_name": (),
            "encryption_type": str,
            "iv": (),
            "encryption_key": ()
        }
        
        # Establish variables
        user_id = authorize_user_id(metadata["username"], metadata["password"])
        file_ids: list = metadata["file_id"]

        # Retrieve file_name, encryption_type, iv and encryption_key from database
        # Establish cursor
        cursor = db_conn.cursor()

        for file_id in file_ids:
            # Write database query
            query = sql.SQL("SELECT file_name, encryption_type, iv, encryption_key FROM FILES WHERE file_id = %s AND user_id = %s")
            cursor.execute(query, (file_id, user_id,))
            result = cursor.fetchone()

            if result:
                # Convert memoryview objects to bytes if necessary
                file_name, encryption_type, iv, encryption_key = result
                iv = bytes(iv) if isinstance(iv, memoryview) else iv
                encryption_key = bytes(encryption_key) if isinstance(encryption_key, memoryview) else encryption_key

                # Append to result_dict
                result_dict["file_name"] += (file_name, )
                result_dict["iv"] += (base64.b64encode(iv).decode('utf-8'), )
                result_dict["encryption_key"] += (base64.b64encode(encryption_key).decode('utf-8'), )
            else:
                print("No Result Found")
                return None
        
        # Finally append encryption_type
        result_dict["encryption_type"] = encryption_type

        # Return the metadata
        return result_dict
    
    except Exception as e:
        print("ERROR: ", e)
        return None
    
    finally:
        # Close cursor
        cursor.close()
