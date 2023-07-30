import requests

seq = 0


def send_updated_data(material, state):
    global seq

    url = 'http://10.5.64.37:5000/'
    new_data = {'value': material, 'date': None, 'seqNumber': seq, 'state': state}
    if new_data['value'] == 'metal' or new_data['value'] == 'plastik':
        seq += 1
    # Send a POST request to update the data
    response = requests.post(url, json=new_data)

    # Check the response
    if response.status_code == 200:
        updated_data = response.json()
        print("Updated data:", updated_data)
    else:
        print("Failed to update data.")

