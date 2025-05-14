result = open("output").read()
temp = bytes.fromhex(result)
target = []
for i in range(0, len(temp), 4):
    target.append(int(temp[i:i+4].hex(), 16))
target = [(a - b) & 0xffffffff for a, b in zip(target[1:], target[:-1])]

# MITM
magic = 0xEDB88320
# build CRCTable
CRCTable = []
for i in range(256):
    tmp = i
    for _ in range(8):
        tmp = (tmp >> 1) ^ (0 if tmp % 2 == 0 else magic)
    CRCTable.append(tmp)

def crc(byte):
    mask = 0xffffffff
    _crc = mask
    for i in byte:
        ind = (_crc ^ i) & 0xff
        _crc = (_crc >> 8) ^ CRCTable[ind]
    _crc = _crc ^ mask
    return _crc

def crc_backward(byte, _crc=0):
    mask = 0xffffffff
    _crc ^= mask
    for i in byte[::-1]:
        ind = [x >> 24 for x in CRCTable].index(_crc >> 24)
        _crc = ((_crc ^ CRCTable[ind]) << 8) ^ (ind ^ i)
    _crc = _crc ^ mask
    return _crc

# this should only take 10 seconds
lookup = {}
for i in range(2 ** 12):
    forward = crc(b"IHDR\0\0" + bytes([i >> 8, i & 255]))
    lookup[forward] = i
lookup_set = set(lookup)

original = []
from rich.progress import track
for entry in track(target):
    little_endian = int(bytes.fromhex(hex(entry)[2:].zfill(8))[::-1].hex(), 16)
    lookup_backward = {}
    for i in range(2 ** 12):
        backward = crc_backward(b"\0\0" + bytes([i >> 8, i & 255]) + b"\x08\x06\0\0\0", little_endian)
        lookup_backward[backward] = i
    intersect = lookup_set & set(lookup_backward)
    assert len(intersect) == 1
    value = list(intersect)[0]
    result = lookup[value] * 2 ** 12 + lookup_backward[value]
    if result == 0xffffff:
        break
    original.append(bytes.fromhex(hex(result)[2:].zfill(6)))
print(b"".join(original).rstrip(b"\r\n").decode())