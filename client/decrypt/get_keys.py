from json import dumps, loads
from requests import post
import uuid
import base64

def get_file_metadata(window: object, file_id: uuid):
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
        "file_id": str(file_id)
    }

    # Convert to Json
    message_json = dumps(message)

    # Request file Metadata
    request_json = post(url, json=message_json, headers=headers)
    response = request_json.json()

    # Deserialize metadata
    metadata_json = response["metadata"]
    metadata: dict = loads(metadata_json)

    print(response["status"])
    print("THIS IS THE METADATA: ", metadata)
    # Convert iv and encryption_key back to bytes
    metadata["iv"], metadata["encryption_key"] = base64.b64decode(metadata["iv"]), base64.b64decode(metadata["encryption_key"])
    
    # Return metadata
    return metadata
    



