from psycopg2 import sql
import psycopg2.extras
import psycopg2

# Check if folder path already exist in the database
def check_folder_path(db_conn: object, metadata: object):
    try:
        # Create a cursor object
        cursor = db_conn.cursor()

        # Define the SQL query for checking if the folder_path exists
        query: str = sql.SQL("SELECT folder_id from folders WHERE folder_path = %s")
        cursor.execute(query, (metadata.folder_path,))
        result = cursor.fetchone()

        # Close the cursor
        cursor.close()

        # Edit folder_id
        if result:
            # Pre Existing Folder_id (Folder details already exists in the database)
            return result[0]
        else: 
            # Folder details dont exist
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return False

# Store the folder metadata in folders table
def store_folder(metadata: object, db_conn: object) -> bool:
    # Make sure psycopg library can handle uuid
    psycopg2.extras.register_uuid()
    
    try:
        # Create a cursor object
        cursor = db_conn.cursor()
        
        # Define the SQL query for inserting data
        insert_query = sql.SQL("""
            INSERT INTO folders (
                folder_id, user_id, folder_path, access_type, parent_folder_id
            ) VALUES (
                %s, %s, %s, %s, %s
            )
        """)
        
        # Execute the SQL query
        cursor.execute(insert_query, (
            metadata.folder_id, metadata.user_id, metadata.folder_path, metadata.access_type, metadata.parent_folder_id
        ))
        
        # Commit the transaction
        db_conn.commit()
        
        # Close the cursor
        cursor.close()
        
        return True
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while inserting folder metadata: {error}")
        # Rollback in case of error
        db_conn.rollback()

        return False