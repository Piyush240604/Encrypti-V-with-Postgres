from authorize import authorize_user_id
from psycopg2 import sql

'''
Function that takes folder_id as parameter
    Checks whether the folder_id is referenced as a parent_folder_id for some record
        Select any record that has that parent_folder_id
        If records exists, then return false
            false indicates that this folder_id cannot be deleted yet, as it would cause foreign key issues
        if record doesn't exist, then return true
            true indicates, that this folder_id is not referenced anywhere, and is free to be deleted 
'''
def check_folder_id(db_conn: object, folder_id) -> bool:
    try:
        # Establish cursor
        cursor: object = db_conn.cursor()

        # Write query to select records
        query = sql.SQL("SELECT folder_id FROM folders WHERE parent_folder_id = %s")
        cursor.execute(query, (folder_id,))
        result = cursor.fetchone()

        if result:
            return False # Folder id is referenced somewhere, cannot delete
        
        return True # Folder id is not referenced, safe to delete
    
    # In case of any errors
    except Exception as e:
        print("Error Occured Checking for existence of parent_folder_id: ", e)
        return False # Since there is an error, best not delete the record
    
    finally:
        # Close cursor
        cursor.close()

# Get the folder_id from database
def get_folder_id(db_conn: object, file_id, user_id):
    try:
        # Establish cursor
        cursor: object = db_conn.cursor()

        # Write select Query
        query: str = sql.SQL("SELECT folder_id FROM files WHERE file_id = %s and user_id = %s")
        cursor.execute(query, (file_id, user_id,))
        result: tuple = cursor.fetchone()

        return result[0]
    
    except Exception as e:
        print("errror: ", e)
        return None
    
    finally:
        # Close cursor
        cursor.close()

# Delete the metadata
def delete_metadata(db_conn: object, metadata: dict) -> bool:
    try:
        # Establish variables for file deletion
        file_ids: list = metadata["file_id"]
        folder_ids = set()
        user_id = authorize_user_id(metadata["username"], metadata["password"])

        for file_id in file_ids:
            
            # Establish cursor
            cursor: object = db_conn.cursor()

            # Get folder_id for the given file id
            folder_ids.add(get_folder_id(db_conn, file_id, user_id))

            # Write the delete query for files table
            query: str = sql.SQL("DELETE FROM files WHERE file_id = %s and user_id = %s")
            cursor.execute(query, (file_id, user_id,))

            # Commit the query
            db_conn.commit()

        # Establish variables for folder deletion
        folder_ids = list(folder_ids)
        length_folder_ids = len(folder_ids)
        deletion_counter = i = 0
        deleted_folder_id_indexes = []

        while deletion_counter < length_folder_ids:
            # Reset i if overflow occurs
            if i >= length_folder_ids:
                i = 0
            
            # Check whether this folder_id has already been processed and deleted
            if i in deleted_folder_id_indexes:
                i += 1
                continue

            # Check whether folder_id is referenced somewhere (if false), increment i, so the loop can check the next folder_id
            if not check_folder_id(db_conn, folder_ids[i]):
                i += 1
                continue
            
            # If we have reached here, the folder_id is safe to be delete
            # Establish cursor
            cursor: object = db_conn.cursor()

            # Write a query
            query = sql.SQL("DELETE FROM folders WHERE folder_id = %s AND user_id = %s")
            cursor.execute(query, (folder_ids[i], user_id,))

            # Commit query
            db_conn.commit()

            # If the deletion is successful
            deletion_counter += 1
            deleted_folder_id_indexes.append(i)
            i += 1

        return True
    
    except Exception as e:
        print("Error: ", e)
        db_conn.rollback()
        return False
    
    finally:
        # Close the cursor
        cursor.close()