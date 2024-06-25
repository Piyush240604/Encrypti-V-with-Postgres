from flask import Flask, request, jsonify
from db_conn import get_db_connection
from store_key_client import store_encryption_key_client

app = Flask(__name__)

@app.route('/file_encryption_client', methods=['POST'])
def file_encryption_client():
    # Get data
    data = request.json

    # Store metadata to database
    store_encryption_key_client(db_conn, data)

    
if __name__ == '__main__':
    # Establish database connection
    db_conn = get_db_connection()

    # Run the slave server
    app.run(port=5001, debug=True)