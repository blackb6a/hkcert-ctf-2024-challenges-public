result = open("output").read()
temp = bytes.fromhex(result)
target = []
for i in range(0, len(temp), 4):
    target.append(int(temp[i:i+4].hex(), 16))
target = [(a - b) & 0xffffffff for a, b in zip(target[1:], target[:-1])]

# MITM
from binascii import crc32 as crc

# this should only take a minute
from rich.progress import track
lookup = {}
for i in track(range(2 ** 12)):
    for j in range(2 ** 12):
        forward = crc(b"IHDR\0\0" + bytes([i >> 8, i & 255]) + b"\0\0" + bytes([j >> 8, j & 255]) + b"\x08\x06\0\0\0")
        lookup[forward] = bytes([i >> 4, ((i & 0xf) << 4 ) | (j >> 8), j & 0xff])

original = []
for entry in track(target):
    little_endian = int(bytes.fromhex(hex(entry)[2:].zfill(8))[::-1].hex(), 16)
    result = lookup[little_endian]
    if result == b"\xff\xff\xff":
        break
    original.append(result)
print(b"".join(original).rstrip(b"\r\n").decode())