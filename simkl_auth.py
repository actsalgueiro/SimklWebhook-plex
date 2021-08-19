import requests
import json
import time

userid = 'USERID'
userToAdd = 'USER'

def get_PIN_code():
    url = f"https://api.simkl.com/oauth/pin?client_id={userid}"

    headers = {
        'Content-Type': 'application/json'
    }

    request_data = json.loads(requests.get(url, headers=headers).text)

    if request_data['result'] == 'OK':
        return request_data
    return None

def retrieveToken(user_code, expires_in, interval):
    url = f"https://api.simkl.com/oauth/pin/{user_code}?client_id={userid}"

    headers = {
        'Content-Type': 'application/json'
    }
    # start polling
    access_token = ''

    t_end = time.time() + expires_in
    while time.time() < t_end:
        request_data = json.loads(requests.get(url, headers=headers).text)
        if 'access_token' in request_data:
            return request_data['access_token']
            break
        time.sleep(interval)
    print("Code expired.")
    return None

def main():
    headers = {
        'Content-Type': 'application/json'
    }

    data = get_PIN_code()
    if data:
        print ("Enter this code at https://simkl.com/pin/: %s" % data['user_code'])
        token = retrieveToken(data['user_code'], data['expires_in'], data['interval'])
    
    # save token at the appropriate folder
    if token:
        with open(f"webhooks/{userToAdd}.txt", "w") as text_file:
            print(f"{token}", file=text_file)
        print("Success.")

if __name__ == "__main__":
    main()