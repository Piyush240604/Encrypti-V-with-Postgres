from flask import Flask, request, jsonify
from db_conn import get_db_connection
from register import register_user

app = Flask(__name__)

# Register user
@app.route('/register', methods=['POST'])
def register():

    if db_conn:
        print("Hello World")
    
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
