result = open("output").read()
temp = bytes.fromhex(result)
target = []
for i in range(0, len(temp), 8):
    target.append(temp[i:i+8])

initial_hash = 0

magic = 0xC96C5795D7870F42
CRCTable = []
for i in range(256):
    tmp = i
    for _ in range(8):
        tmp = (tmp >> 1) ^ (0 if tmp % 2 == 0 else magic)
    CRCTable.append(tmp)

def crc(byte):
    mask = 0xffffffffffffffff
    _crc = mask
    for i in byte:
        ind = (_crc ^ i) & 0xff
        _crc = (_crc >> 8) ^ CRCTable[ind]
    _crc ^= mask
    return _crc

def break_crc(target, prefix=b""):
    mask = 0xffffffffffffffff
    initial = crc(prefix) ^ mask
    target ^= mask
    _crc = target
    for _ in range(64 >> 3):
        ind = [x >> (64 - 8) for x in CRCTable].index(_crc >> (64 - 8))
        _crc = ((_crc ^ CRCTable[ind]) << 8) ^ ind
    _crc ^= initial
    return bytes.fromhex(hex(_crc)[2:].zfill(64 >> 2))[::-1]

lookup = {}
from rich.progress import track
pos_set = set()
for pre in track(target):
    for pos in target:
        if pre == pos:
            continue
        little_endian = int(bytes.fromhex(pos.hex())[::-1].hex(), 16)
        attempt = break_crc(little_endian, pre)
        if attempt[-2:] == b"\xff\xff":
            lookup[pre] = (pos, attempt[:-2])
            pos_set.add(pos)

# find the one without being a pos
header = set(target) - pos_set
assert len(header) == 1
header = list(header)[0]
original = []
while header in lookup:
    next, result = lookup[header]
    original.append(result)
    if b"\0" in result:
        break
    header = next
print(b"".join(original).rstrip(b"\0").decode())