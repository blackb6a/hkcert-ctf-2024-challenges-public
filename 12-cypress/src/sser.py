import os
import requests
from Crypto.Cipher import AES
import hashlib

def get_nonce():
    while True:
        nonce = os.urandom(16)
        if hashlib.sha256(b'pow/' + nonce).digest()[:3] == b'\0\0\0': return nonce

flag = input('What is the flag?> ').encode()
nonce = get_nonce()

r = requests.post('https://c12-cypress.hkcert24.pwnable.hk/', json={
    'nonce': nonce.hex()
})
c0 = bytes.fromhex(r.text)

key = hashlib.sha256(b'key/' + nonce).digest()[:16]
iv = hashlib.sha256(b'iv/' + nonce).digest()[:16]
cipher = AES.new(key, AES.MODE_CFB, iv)
c1 = cipher.encrypt(flag)

print('🙆🙅'[c0 != c1])
