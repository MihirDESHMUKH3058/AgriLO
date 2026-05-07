import urllib.request
import json

data = json.dumps({
    "name": "Ram patil",
    "email": "admin@gmail.com",
    "password": "testpassword",
    "phone": "+91 8574652315",
    "language": "en"
}).encode('utf-8')

req = urllib.request.Request("http://localhost:10000/api/auth/register", data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("Body:", response.read().decode())
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print("Error Body:", e.read().decode())
except Exception as e:
    print("Exception:", str(e))
