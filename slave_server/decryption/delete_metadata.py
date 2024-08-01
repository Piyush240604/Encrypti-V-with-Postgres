from authorize import authorize_user_id
from psycopg2 import sql

# Get the folder_id from database
def get_folder_id(db_conn: object, file_id, user_id):
    try:
        # Establish cursor
        cursor: object = db_conn.cursor()

        # Write select Query
        query: str = sql.SQL("SELECT folder_id FROM files WHERE file_id = %s and user_id = %s")
        cursor.execute(query, (file_id, user_id,))
        result: tuple = cursor.fetchone()

        # Close cursor
        cursor.close()

        return result[0]
    
    except Exception as e:
        print("errror: ", e)
        return None

# Delete the metadata
def delete_metadata(db_conn: object, metadata: dict) -> bool:
    try:
        # Establish variables
        file_id: str = metadata["file_id"]
        user_id = authorize_user_id(metadata["username"], metadata["password"])
        print("VARIABLES: ", file_id, user_id)

        # Get folder ID
        folder_id = get_folder_id(db_conn, file_id, user_id)

        # Check if folder_id was properly receieved
        if not folder_id:
            return False
        
        # Establish cursor
        cursor: object = db_conn.cursor()

        # Write the delete query for files table
        query: str = sql.SQL("DELETE FROM files WHERE file_id = %s and user_id = %s")
        cursor.execute(query, (file_id, user_id,))

        # Commit the query
        db_conn.commit()
        
        # Write the delete query for folders table
        query = sql.SQL("DELETE FROM folders WHERE folder_id = %s and user_id = %s")
        cursor.execute(query, (folder_id, user_id,))

        # Commit the query
        db_conn.commit()

        # Close the cursor
        cursor.close()

        return True
    
    except Exception as e:
        print("Error: ", e)
        db_conn.rollback()
        return False