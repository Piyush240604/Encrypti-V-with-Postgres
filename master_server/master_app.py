from flask import Flask, request, jsonify
from db_conn import get_db_connection
from authorize import authorize
from register import register_user

app = Flask(__name__)

# Login User
@app.route('/login', methods=['POST'])
def login():
    # Get the user-details
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    # Authorize the data
    user_id = authorize(db_conn, username, password)

    # Return User_ID
    return jsonify({'user_id': user_id})

# Register user
@app.route('/register', methods=['POST'])
def register():
    # Get the user-details
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    # Register Data to the database
    registration = register_user(db_conn, username, password)

    # Check whether it was successfully registered
    if registration == 'S':
        return jsonify({'message': 'User Registered Successfully'})
    else:
        return jsonify({'message': str(registration)})

if __name__ == '__main__':

    # Establish database connection
    db_conn = get_db_connection()

    # Run the master server
    app.run(port=5000, debug=True)
