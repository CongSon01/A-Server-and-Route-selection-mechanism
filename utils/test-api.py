import requests

url = "http://localhost:5000/write_data/"

data = {
    "src": "A",
    "dst": "B",
    "delay": 5.6,
    "packetLossRate": 0.3,
    "linkUtilization": 0.7,
    "byteSent": 100,
    "byteReceived": 200
}
response = requests.post(url, data)

# print(response.json())

