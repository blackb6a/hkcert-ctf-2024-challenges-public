import os
import random
from pwn import *

from aes import sub_bytes, inv_sub_bytes, \
                shift_rows, inv_shift_rows, \
                mix_columns, inv_mix_columns, \
                bytes2matrix, matrix2bytes

# Generate a good seed
attempt = 0
operations = ['ark'] + sum([['sb', 'sr', 'mc', 'ark'] for _ in range(1, 14)], []) + ['sb', 'sr', 'ark']
while True:
    attempt += 1
    if attempt % 100000 == 0: print(f'[ ] attempt #{attempt}')

    seed = os.urandom(16)
    random.seed(seed)
    selected_operations = random.choices(operations, k=len(operations))
    if selected_operations.count('ark') != 1: continue
    break

print(f'[*] {seed, selected_operations = }')

# ===

def derive_ark_from_m_and_c(m, c, selected_operations):
    s, t = bytes2matrix(m), bytes2matrix(c)

    for operation in selected_operations:
        if operation == 'ark': break

        if   operation == 'sb': sub_bytes(s)
        elif operation == 'sr': shift_rows(s)
        elif operation == 'mc': mix_columns(s)

    for operation in selected_operations[::-1]:
        if operation == 'ark': break

        if   operation == 'sb': inv_sub_bytes(t)
        elif operation == 'sr': inv_shift_rows(t)
        elif operation == 'mc': inv_mix_columns(t)

    return xor(matrix2bytes(s), matrix2bytes(t))


r = remote('localhost', 28106)

r.sendlineafter('🌱 '.encode(), seed.hex().encode())

r.recvuntil('🤐 '.encode())
c0 = bytes.fromhex(r.recvline().decode())

m1 = b'\0'*16
r.sendlineafter('💬 '.encode(), m1.hex().encode())
r.recvuntil('🤫 '.encode())
c1 = bytes.fromhex(r.recvline().decode())
x = derive_ark_from_m_and_c(m1, c1, selected_operations)

# recover m0
m0 = bytes2matrix(c0)
for operation in selected_operations[::-1]:
    if   operation == 'ark': m0 = bytes2matrix(xor(matrix2bytes(m0), x))
    elif operation == 'sb':  inv_sub_bytes(m0)
    elif operation == 'sr':  inv_shift_rows(m0)
    elif operation == 'mc':  inv_mix_columns(m0)

m0 = matrix2bytes(m0)

r.sendlineafter('💬 '.encode(), m0.hex().encode())
r.interactive()
