with open('../flag.enc', 'rb') as f:
    bmp = bytearray(f.read())

# estimate from lines 22 and 23
width = 1024
height = 1024

bmp[ 0: 2] = b'BM'
bmp[ 2: 6] = int.to_bytes(54 + width*height*3, 4, 'little') # file size
bmp[ 6:10] = b'\0\0\0\0'
bmp[10:14] = int.to_bytes(54, 4, 'little') # data start

# header
bmp[14:18] = int.to_bytes(0x28, 4, 'little') # header size
bmp[18:22] = int.to_bytes(height, 4, 'little') # height
bmp[22:26] = int.to_bytes(width, 4, 'little') # width
bmp[26:28] = int.to_bytes(0x1, 2, 'little') # nb plan
bmp[28:30] = int.to_bytes(0x18, 2, 'little') # bpp
bmp[30:34] = int.to_bytes(0, 4, 'little') # compression
bmp[34:38] = int.to_bytes(3*height*width, 4, 'little') # image size

print(len(bmp))
print(54 + width*height*3)

with open('flag.bmp', 'wb') as f: f.write(bmp)
