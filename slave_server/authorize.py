import requests

def authorize_user_id(username, password) -> str:
    # Establish URL and data to be sent to master server
    url: str = "http://127.0.0.1:5000/login"
    headers: dict = {
        "Content-Type": "application/json"
    }
    payload: dict = {
        "username": username,
        "password": password
    }
    
    # Get response
    response = requests.post(url, json=payload, headers=headers)

    # Check response
    if response:
        # Get user_id
        user_id = response.json().get("user_id")
        return user_id[0]
    else:
        print("Error:", response.json().get("error"))