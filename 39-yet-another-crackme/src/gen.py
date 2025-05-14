import random
import string
# def genmap():
#     x = [i for i in string.printable]
#     y = [i for i in string.printable]
#     m = {}
#     while len(x) != 0:
#         t = random.choice(x)
#         m[ord(y.pop())] = ord(t)
#         x.remove(t)
#     return m
# M = genmap()

FLAG = "hkcert24{f0r3v3r_r3m3mb3r_x4m4r1n_2024-5-1}"

M = {12: 88, 11: 66, 13: 78, 10: 38, 9: 58, 32: 39, 126: 57, 125: 40, 124: 83, 123: 62, 96: 95, 95: 84, 94: 73, 93: 91, 92: 94, 91: 50, 64: 104, 63: 107, 62: 74, 61: 121, 60: 55, 59: 11, 58: 77, 47: 112, 46: 56, 45: 33, 44: 93, 43: 126, 42: 59, 41: 42, 40: 32, 39: 98, 38: 49, 37: 48, 36: 106, 35: 64, 34: 125, 33: 80, 90: 70, 89: 72, 88: 52, 87: 114, 86: 122, 85: 113, 84: 76, 83: 90, 82: 92, 81: 54, 80: 75, 79: 115, 78: 89, 77: 103, 76: 51, 75: 47, 74: 12, 73: 81, 72: 97, 71: 102, 70: 41, 69: 34, 68: 110, 67: 46, 66: 63, 65: 65, 122: 109, 121: 86, 120: 79, 119: 99, 118: 69, 117: 118, 116: 105, 115: 71, 114: 119, 113: 43, 112: 37, 111: 100, 110: 123, 109: 116, 108: 85, 107: 67, 106: 96, 105: 44, 104: 13, 103: 9, 102: 101, 101: 108, 100: 53, 99: 124, 98: 82, 97: 36, 57: 61, 56: 68, 55: 10, 54: 35, 53: 87, 52: 45, 51: 111, 50: 117, 49: 60, 48: 120}
KEY = 0xCAFEBABECAFEBABE
BLOCKSIZE = 8
s1 = ""
for i in FLAG:
    s1 += chr(M[ord(i)])
pad_size = BLOCKSIZE-(len(FLAG)%BLOCKSIZE)
a = s1+"\x01"*pad_size
s2 = []
for i in range(0,len(a)-1,BLOCKSIZE):
    b = int.from_bytes(f"{a[i:i+BLOCKSIZE]}".encode(),"little")
    s2.append(b)
s3 = []
for block in s2:
    t = KEY
    t = block ^ t
    s3.append(t)

m1 = []
m2 = []
x = list(M.keys())
x.sort()
for i in x:
    m1.append(i)
    m2.append(M[i])
print(m1)
print(m2)
print(s3)