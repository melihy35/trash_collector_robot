import requests

def send_updated_data(url, new_data):
    # Send a POST request to update the data
    response = requests.post(url, json=new_data)

    # Check the response
    if response.status_code == 200:
        updated_data = response.json()
        print("Updated data:", updated_data)
    else:
        print("Failed to update data.")
def send_state(url, new_data):
    # Send a POST request to update the data
    response = requests.post(url, json=new_data)

    # Check the response
    if response.status_code == 200:
        updated_data = response.json()
        print("Updated data:", updated_data)
    else:
        print("Failed to update data.")        

if __name__ == "__main__":
    # Replace 'http://localhost:5000' with the appropriate URL of your server
    url = 'http://localhost:5000/'

    # Data to update
    new_data = {'value': 'metal','date': None,'seqNumber': 1}
    initialState = {'state' : 'Araniyor..'}
    foundState = {'state' : "Found"}
    # Call the function to send the updated data
    send_state(url,initialState)
    send_updated_data(url, new_data)
    send_state(url,foundState)
    