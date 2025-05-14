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
    selected_operations = operations[:]
    random.shuffle(selected_operations)

    first = selected_operations.index('ark')
    last = 4*14 - selected_operations[::-1].index('ark')
    if selected_operations[first:last].count('mc') != 0: continue

    break

print(f'[*] {seed, selected_operations = }')

# ===

def derive_t_from_c(c, selected_operations):
    t = bytes2matrix(c)

    for operation in selected_operations[::-1]:
        if operation == 'ark': break

        if   operation == 'sb': inv_sub_bytes(t)
        elif operation == 'sr': inv_shift_rows(t)
        elif operation == 'mc': inv_mix_columns(t)

    return matrix2bytes(t)

def get_m_from_s(s, selected_operations):
    s = bytes2matrix(s)
    first = selected_operations.index('ark')
    for operation in selected_operations[first-1::-1]:
        assert operation != 'ark'
        if   operation == 'sb': inv_sub_bytes(s)
        elif operation == 'sr': inv_shift_rows(s)
        elif operation == 'mc': inv_mix_columns(s)
    return matrix2bytes(s)


r = remote('localhost', 38106)

r.sendlineafter('🌱 '.encode(), seed.hex().encode())

r.recvuntil('🤐 '.encode())
c0 = bytes.fromhex(r.recvline().decode())
t0 = derive_t_from_c(c0, selected_operations)

mapper = {}
# mapper[t_pos, t_val] = (s_pos, s_val)

s = bytearray(b'\0'*16)
m = get_m_from_s(s, selected_operations)
r.sendlineafter('💬 '.encode(), m.hex().encode())
r.recvuntil('🤫 '.encode())
c1 = bytes.fromhex(r.recvline().decode())
t1 = derive_t_from_c(c1, selected_operations)

for i in range(16):
    for j in range(1, 256):
        s = bytearray(b'\0'*16)
        s[i] = j
        m = get_m_from_s(s, selected_operations)
        r.sendline(m.hex().encode())

    # ===

    for j in range(1, 2):
        r.recvuntil('🤫 '.encode())
        c = bytes.fromhex(r.recvline().decode())
        t = derive_t_from_c(c, selected_operations)

        id = [t1_ != t_ for t1_, t_ in zip(t1, t)].index(True)

        mapper[id, t1[id]] = (i, 0)
        mapper[id, t[id] ] = (i, 1)

    for j in range(2, 256):
        r.recvuntil('🤫 '.encode())
        c = bytes.fromhex(r.recvline().decode())
        t = derive_t_from_c(c, selected_operations)
        mapper[id, t[id] ] = (i, j)

s0 = bytearray(16)
for i in range(16):
    j, m = mapper[i, t0[i]]
    s0[j] = m
m0 = get_m_from_s(s0, selected_operations)

print(f'{m0.hex() = }')
print(f'{c0.hex() = }')
r.sendlineafter('💬 '.encode(), m0.hex().encode())
r.interactive()
