from hash_password import hash_password

def authorize(db_conn, username, password):
    try:
        # Establish cursor
        db_cur = db_conn.cursor()
        db_cur.execute("""
            SELECT User_id FROM USERS WHERE Username = %s AND Password = %s
        """, (username, hash_password(password)))
        result = db_cur.fetchone()
        db_cur.close()

        # Return user_id
        return result
    except Exception as e:
        return e