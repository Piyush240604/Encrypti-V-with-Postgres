from json import dumps, loads
from requests import post
import base64

def get_file_metadata(window: object, file_ids: list):
    # Initialize URL and headers for POST
    url: str = "http://127.0.0.1:5001/decryption_client"

    headers: dict = {
        "Content-Type": "application/json"
    }

    # Establish details to send to server
    username: str = window.username_field.text()
    password: str = window.password_field.text()

    # Formulate message
    message: dict = {
        "username": username,
        "password": password,
        "file_id": file_ids
    }

    # Convert to Json
    message_json = dumps(message)

    # Request file Metadata
    request_json = post(url, json=message_json, headers=headers)
    response = request_json.json()

    # Deserialize metadata
    metadata_json = response["metadata"]
    if metadata_json == "None":
        return None

    metadata: dict = loads(metadata_json)

    if not response["status"]:
        return {}
    
    # Convert iv and encryption_key back to bytes
    metadata["iv"] = [base64.b64decode(iv) for iv in metadata["iv"]]
    metadata["encryption_key"] = [base64.b64decode(encryption_key) for encryption_key in metadata["encryption_key"]]

    # Return metadata
    return metadata
    



