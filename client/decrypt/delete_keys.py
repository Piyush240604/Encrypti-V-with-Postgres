from json import dumps
from requests import post

def delete_record(window: object, file_id: list) -> bool:
    # Initialize URL and headers for POST
    url: str = "http://127.0.0.1:5001/delete_record"

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
        "file_id": file_id
    }

    # Convert to Json
    message_json = dumps(message)

    # Request file Metadata
    request_json = post(url, json=message_json, headers=headers)
    response = request_json.json()


    return response['status']