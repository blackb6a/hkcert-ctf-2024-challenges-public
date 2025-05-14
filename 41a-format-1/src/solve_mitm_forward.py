result = open("output").read()
temp = bytes.fromhex(result)
target = []
for i in range(0, len(temp), 4):
    target.append(int(temp[i:i+4].hex(), 16))
target = [(a - b) & 0xffffffff for a, b in zip(target[1:], target[:-1])]


from binascii import crc32

# this time use the famous relationship: crc(a ^ b ^ c) = crc(a) ^ crc(b) ^ crc(c)
# this does not require the backward function, which means we can just use binascii.crc32
dummy = crc32(b"\0" * 17)
# i = 1234
# j = 5678
# forward = crc32(b"IHDR\0\0" + bytes([i >> 8, i & 255]) + b"\0" * 9)
# backward = crc32(b"\0" * 8 + b"\0\0" + bytes([j >> 8, j & 255]) + b"\x08\x06\0\0\0") ^ dummy
# all_in_one = crc32(b"IHDR\0\0" + bytes([i >> 8, i & 255]) + b"\0\0" + bytes([j >> 8, j & 255]) + b"\x08\x06\0\0\0")
# assert forward ^ backward == all_in_one

# this should finish in about 1 second (and should also recover the unused parts if the break statement is removed)
lookup = {}
for i in range(2 ** 12):
    forward = crc32(b"IHDR\0\0" + bytes([i >> 8, i & 255]) + b"\0" * 9)
    lookup[forward] = i
lookup_set = set(lookup)
lookup_backward = {}
for i in range(2 ** 12):
    backward = crc32(b"\0" * 10 + bytes([i >> 8, i & 255]) + b"\x08\x06\0\0\0") ^ dummy
    lookup_backward[backward] = i

original = []
from rich.progress import track
for entry in track(target):
    little_endian = int(bytes.fromhex(hex(entry)[2:].zfill(8))[::-1].hex(), 16)
    lookup_backward_temp = {key ^ little_endian: value for key, value in lookup_backward.items()}
    intersect = lookup_set & set(lookup_backward_temp)
    value = list(intersect)[0]
    result = lookup[value] * 2 ** 12 + lookup_backward_temp[value]
    if result == 0xffffff:
        break
    original.append(bytes.fromhex(hex(result)[2:].zfill(6)))
print(b"".join(original).rstrip(b"\r\n").decode())