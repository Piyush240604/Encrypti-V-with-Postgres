import hashlib
import uuid

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(db_conn, username, password):
    try:
        # Establish cursor
        db_cur = db_conn.cursor()

        # Generate user_id
        user_id = str(uuid.uuid4())

        # Execute query
        db_cur.execute("""
            INSERT INTO USERS (User_id, Username, Password)
            VALUES (%s, %s, %s)
        """, (user_id, username, hash_password(password)))

        # Commit query
        db_conn.commit()
        
        # Close cursor
        db_cur.close()

        return "S" # S for Successful
    except Exception as e:
        return e # U for Unsuccessful