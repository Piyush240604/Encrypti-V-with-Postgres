from psycopg2 import sql
import psycopg2.extras
import psycopg2

# Store the file metadata in files table
def store_file(db_conn: object, metadata: object) -> bool:
    # Make sure psycopg library can handle uuid
    psycopg2.extras.register_uuid()

    try:
        # Establish cursor
        cursor = db_conn.cursor()
        print(metadata.file_id, metadata.user_id, metadata.folder_id, metadata.file_name, metadata.encryption_type, metadata.date_encrypted, metadata.iv, metadata.encryption_key, metadata.access_type)

        # Write the insert query
        insert_query = sql.SQL("""
        INSERT INTO files (
            file_id, user_id, folder_id, file_name, encryption_type, date_encrypted, iv, encryption_key, access_type
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """)

        # Execute Insert Query
        cursor.execute(insert_query, (
            metadata.file_id, metadata.user_id, metadata.folder_id, metadata.file_name, metadata.encryption_type, metadata.date_encrypted, metadata.iv, metadata.encryption_key, metadata.access_type
        ))

        # Commit the Transaction
        db_conn.commit()

        # Close the cursor
        cursor.close()

        # Return true
        return True
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while inserting file metadata: {error}")
        # Rollback in case of error
        db_conn.rollback()

        # Return false
        return False