from pwn import *
import json

def xor(a, b):
    return bytes(u^v for u, v in zip(a, b))

def check_flag(r, ciphertext):
    res = json.dumps({
        "type": "communicate",
        "ciphertext": ciphertext.hex()
    }, separators=(',', ':'))
    r.sendlineafter('🕊️'.encode(), f'byron {res}'.encode())

    res = r.recvline().strip().decode()
    r.sendlineafter('🕊️'.encode(), f'alice {res}'.encode())

    res = r.recvline().strip().decode()
    j = json.loads(res)
    return len(bytes.fromhex(j.get('ciphertext'))) == 8+2


r = remote('localhost', 38124)

r.recvline()
r.recvline()

# Alice -> Byron: done!
res = r.recvline().strip().decode()
r.sendlineafter('🕊️'.encode(), f'byron {res}'.encode())

# Byron -> Alice: what is the flag?
res = r.recvline().strip().decode()
r.sendlineafter('🕊️'.encode(), f'alice {res}'.encode())

# Alice -> Byron: the flag is...
res = r.recvline().strip().decode()
j = json.loads(res)
ciphertext = bytearray.fromhex(j.get('ciphertext'))

flag_prefix = b'hkcert24{'
while len(flag_prefix) < len(ciphertext)-20:
    flag_target = flag_prefix+b'}'
    for x in range(128):
        flag_guess = flag_prefix + bytes([x])
        # the prepending null bytes are:
        # - 8 bytes of nonce,
        # - 12 bytes of "the flag is "
        ciphertext_guess = xor(ciphertext, b'\0'*20+xor(flag_guess, flag_target))
        if not check_flag(r, ciphertext_guess): continue
        break
    else:
        assert False, 'skill issue'
    flag_prefix = flag_guess
    print(flag_prefix)
