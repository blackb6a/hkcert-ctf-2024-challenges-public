from PIL import Image, ImageDraw
from random import randint

# Constants
width, height = 480, 360
square_size = 20
center_x = 0
center_y = 0

color_0 = '#0000ff'
color_1 = '#ff0000'

def chr2bin(c):
    return '{:08b}'.format(min(ord(c), 255)) # prevent > 255 values

def plot(draw: ImageDraw.ImageDraw, x, y, color: int):
    # Adjust input coordinates (convert from origin in the middle to top-left origin)
    canvas_center_x = width // 2
    canvas_center_y = height // 2 - 1 # scratch... why do this to me... -1...
    adjusted_x = canvas_center_x + x
    adjusted_y = canvas_center_y - y  # Invert Y-axis to match drawing convention

    if color == 1:
        draw.point((adjusted_x, adjusted_y), color_1)
    else:
        draw.point((adjusted_x, adjusted_y), color_0)

def gen(filename, text):
    # Create a blank image with a white background
    # img = Image.new('RGB', (width, height), 'white')
    img = Image.open('er.png')
    draw = ImageDraw.Draw(img)
    text = text.upper() # scratch does not support case sensitive
    text_in_binary = ''.join([ chr2bin(x) for x in text ])
    print(text_in_binary)

    def get_text_in_binary(idx: int): # scratch is 1-based index
        return int(text_in_binary[idx-1:idx:1] or 0)

    ## main draw
    r = 24
    p = 1
    while not (p > len(text_in_binary)):
        i = r * -1
        for _ in range(r * 2 + 1): # correct?
            y = i
            x1 = abs(y) - r
            x2 = r - abs(y)
            plot(draw, x1, y, get_text_in_binary(p))
            p += 1
            if not (x1 == x2):
                plot(draw, x2, y, get_text_in_binary(p))
                p += 1
            i += 1
        r += 1

    # Save the image
    img.save(filename)

if __name__ == '__main__':
    file_count = 500
    flag = 'HKCERT24{ERRR_C0DING_EX3RC1SE}'

    dummy_text = open('dummy.txt', 'r').read()
    
    # insert flag
    pos = randint(0, len(dummy_text) - 1)
    dummy_text = ''.join((dummy_text[:pos], ' ', flag, ' ', dummy_text[pos:]))

    total_length = len(dummy_text)
    size = total_length // file_count

    for i in range(1, file_count + 1):
        print(dummy_text[(i-1)*size:i*size])
        gen('gen/{}.png'.format(i), dummy_text[(i-1)*size:i*size])
        break