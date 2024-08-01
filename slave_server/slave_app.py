from flask import Flask, request, jsonify
from db_conn import get_db_connection
from decryption.delete_metadata import delete_metadata
from decryption.retrieve_keys import retrieve_keys
from encryption.store_metadata import store_encryption_key_client
import json
import uuid

app = Flask(__name__)

# Client Encryption
@app.route('/encryption_client', methods=['POST'])
def encryption_client():
    # Get data
    metadata_json = request.json

    # Deserialize the data
    metadata = json.loads(metadata_json)

    # Store metadata to database and receive file_id
    file_id: uuid = store_encryption_key_client(db_conn=db_conn, received_metadata=metadata)

    # Check if storage was successful
    if file_id:
        status = True
    else:
        status = False

    return jsonify({"status": status, "file_id": file_id})

# Client Decryption
@app.route('/decryption_client', methods=['POST'])
def decryption_client():
    # Receive message
    message_json = request.json

    # Deserialize the data
    message: dict = json.loads(message_json)

    metadata: dict = retrieve_keys(db_conn=db_conn, metadata=message)
    
    # Check if Metadata is present
    if metadata:
        # Status is success
        status: str = "success!"
        
        # Serialize the tuple
        metadata_json = json.dumps(metadata)

    else:
        status: str = "Failed!"
        metadata_json = "None"
        
    
    return jsonify({"status" : status, "metadata": metadata_json})

# Decryption Metadata deletion
@app.route('/delete_record', methods=['POST'])
def delete_record():
    print("INSIDE DELETE RECORD")
    # Receive message
    message_json = request.json

    # Deserialize the message
    message: dict = json.loads(message_json)

    deletion: bool = delete_metadata(db_conn=db_conn, metadata=message)

    return jsonify({"status": deletion})
    
if __name__ == '__main__':
    # Establish database connection
    db_conn = get_db_connection()

    # Run the slave server
    app.run(port=5001, debug=True, threaded=True)