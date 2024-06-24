import requests
import re

# Function to check if a password is strong
def is_strong_password(password):
    return password is not None and re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[_@#$%^&+=!]).{8,}$", password)


def client_register_user(window, username, password):

    print(username, password)
    print(type(username))

    # Check if username or password is entered
    if username == '' or password == '':
        window.show_message("Enter a Valid Username and password.")
    
    # If Password is not strong
    elif not is_strong_password(password):
        window.show_message("Enter a Strong password.")
    
    else:
        # Establish url and data to be sent to master server
        url = "http://localhost:5000/register"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response:
            print(response.json().get('message'))
            window.show_message("Registration successful. You can now log in")
            return 
        else:
            print("Error:", response.json().get("error"))