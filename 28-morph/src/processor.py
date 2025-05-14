
from pwn import *

f = open('./a.out', 'rb')

raw_binary = f.read()

f.close()

raw_binary = bytearray(raw_binary)

binary = ELF('./a.out')

fn_key = b'2ps5y\x96T\x8aj9\x90\xd6+\xa3\x07\x00\x1e)d\x92S\xb6\xf5\xc7\x8a\xeb\x7f\xfe\x8a\x81\x03\x88s\x945<\x1d(G\x15\xbd\xd2CU\xd8l\x01\xaf\xe4\xab\xa7\xdc0\xd5'

mapping = {}

for i in range(54):
    sym = ""
    test_sym = f"_Z9verify_{i}RNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE"
    if test_sym in binary.symbols:
        sym = test_sym
    else:
        sym = f"_Z8verify_{i}RNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE"
    mapping[i] = (binary.symbols[sym])
    
    file_offset = binary.vaddr_to_offset(mapping[i])

    for j in range(0x56):
        raw_binary[file_offset + j] ^= fn_key[i]

with open('morph', 'wb') as f:
    f.write(raw_binary)
