from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os 
TEMP_DIR = "test"

with open("flag.enc","rb") as fp:
    ct = fp.read()


os.mkdir(TEMP_DIR)
def guessHeaders(width : int, height : int, numBits : int):
    # Bitmap file header
    # 2 bytes The header field used to identify the BMP and DIB file is 0x42 0x4D
    # 4 bytes The size of the BMP file in bytes
    # 2 bytes can be 0
    # 2 bytes can be 0
    # 4 bytes The offset, i.e. starting address, of the byte where the bitmap image data (pixel array) can be found. Length of the header. 0 also works but you can also fix it
    header = b"\x42\x4D"+ len(ct).to_bytes(4, 'little') + 0x0.to_bytes(2, 'little') + 0x0.to_bytes(2, 'little') + 0x0.to_bytes(4, 'little')

    # DIB header
    # 4	the size of this header, in bytes (40)
    # 4	the bitmap width in pixels (signed integer)
    # 4	the bitmap height in pixels (signed integer)
    # 2	the number of color planes (must be 1)
    # 2	the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
    # 4	the compression method being used. See the next table for a list of possible values. 0	BI_RGB	none	Most common
    # 4	the image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
    # 4	the horizontal resolution of the image. (pixel per metre, signed integer) 0 works
    # 4	the vertical resolution of the image. (pixel per metre, signed integer) 0 works
    # 4	the number of colors in the color palette, or 0 to default to 2n
    # 4	the number of important colors used, or 0 when every color is important; generally ignored
    header += 0x28.to_bytes(4, 'little') + width.to_bytes(4, 'little') + height.to_bytes(4, 'little') + 0x1.to_bytes(2, 'little') + numBits.to_bytes(2, 'little') + 0x0.to_bytes(4, 'little') + 0x0.to_bytes(4, 'little') + 0x0.to_bytes(4, 'little') + 0x0.to_bytes(4, 'little') + 0x0.to_bytes(4, 'little') + 0x0.to_bytes(4, 'little')

    return header
for w in range(0,0x500,0x100):
    for h in range(0,0x500,0x100):
        for nb in [1,4,8,16,24,32]:
            with open(TEMP_DIR + f"/flag_{w}_{h}_{nb}.enc.bmp","wb") as fp:
                g = guessHeaders(w,h,nb)
                fp.write(g+ct[len(g):])

