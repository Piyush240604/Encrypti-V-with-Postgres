import requests

def client_login_user(window, username, password):
    # Establish URL and data to be sent to master server
    url = "http://localhost:5000/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password
    }
    
    # Get response
    response = requests.post(url, json=payload, headers=headers)
    
    if response:
        # Get user_id
        user_id = response.json().get("user_id")

        # Verify User_id
        if user_id:
            window.show_message("Login successful!")
            print("User ID:", user_id, "\nType: ", type(user_id))
            
            # Go to next page
            window.hide_components(2)
            window.show_buttons()
        else:
            window.show_message("Login failed: Invalid username or password.")
    else:
        print("Error:", response.json().get("error"))