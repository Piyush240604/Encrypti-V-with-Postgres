def get_parent_folder_id(db_conn: object, folder_path: str):
    try:
        # Establish cursor
        cursor = db_conn.cursor()

        # Write the query
        query = "SELECT folder_id FROM folders WHERE folder_path = %s"

        # Execute the query
        cursor.execute(query, (folder_path, ))

        # Fetch the result
        result = cursor.fetchone()

        # If result exists, return the parent_
        if result:
            parent_folder_id = result[0]
            return parent_folder_id
    
    except Exception as e:
        print("ERror: ", e)
    
    finally:
        # Close the cursor
        cursor.close()