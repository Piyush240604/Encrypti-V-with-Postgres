from datetime import datetime

def get_datetime() -> str:
    # Get the current timestamp
    date_encrypted = datetime.now()

    # Format the timestamp as string (if required by your database library)
    date_encrypted_str: str = date_encrypted.strftime('%Y-%m-%d %H:%M:%S')

    return date_encrypted_str
