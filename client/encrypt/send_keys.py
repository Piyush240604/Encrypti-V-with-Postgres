from json import dumps
from requests import post

# Function to send metadata to slave server
def send_keys(encryption_metadata):
    url = "http://127.0.0.1:5001/encryption_client"

    headers = {
        "Content-Type": "application/json"
    }

    # Serialize the data to JSON
    encryption_metadata_json = dumps(encryption_metadata)

    # Send details to the server and receive confirmation using requests
    response_json = post(url, json=encryption_metadata_json, headers=headers)
    response_data = response_json.json()
    print(response_data)

    # See if the status is successful
    if response_data["status"]:
        # Return file ID
        return response_data["file_id"]
    else:
        # Error in status which means there was an issue in metadata storage
        return "E"