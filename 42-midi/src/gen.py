import random
random.seed(30624700)
flag = "hkcert24{b3t_U_h4v3_go0d_h34r1n9_"
flag += hex(random.randrange(2 ** 64))[2:].zfill(16)
flag += "}"
print("Flag:", flag)
flag = flag.encode()
mix = [0] * 9
mix.extend([random.randint(-2, 2) for _ in range(len(flag) - len("hkcert24{}"))])
mix.append(0)
print("Mix:", mix)

def export(fn, notes, mix_values = None):
    if mix_values is None:
        mix_values = [0] * len(notes)
    assert len(mix_values) == len(notes)
    with open(fn, "wb") as f:
        f.write(b"MThd")
        f.write(b"\x00\x00\x00\x06") # header length
        f.write(b"\x00\x00") # format: 1 track
        f.write(b"\x00\x01") # ntrks: 1 track
        f.write(b"\x00\x01") # division: ticks per quarter note
        f.write(b"MTrk") # track header
        from io import BytesIO
        f2 = BytesIO()
        for i in range(len(notes)):
            if mix_values[i] != 0:
                f2.write(b"\x00") # delta-time: 0
                f2.write(b"\xe0") # pitch wheel change, channel 0
                if mix_values[i] == -2:
                    f2.write(b"\x7f\x7f") # 32767
                else:
                    f2.write(b"\x00")
                    f2.write(bytes([(2 - mix_values[i]) * 32]))
            velocity = round(127 - 63 * (i / len(notes)))
            f2.write(b"\x00") # delta-time: 0
            f2.write(b"\x90") # note on, channel 0
            pitch = notes[i] + mix_values[i]
            assert 0 <= pitch < 128 
            f2.write(bytes([pitch, velocity])) # pitch, velocity
            f2.write(b"\x01") # delta-time: 1
            f2.write(b"\x80") # note off, channel 0
            f2.write(bytes([pitch, velocity])) # pitch, velocity
            if mix_values[i] != 0 and (i != len(notes) - 1 and mix_values[i + 1] == 0):
                f2.write(b"\x00") # delta-time: 0
                f2.write(b"\xe0") # pitch wheel change, channel 0
                f2.write(b"\x00\x40") # 64
        f2.write(b"\x00") # delta-time: 0
        f2.write(b"\xff\x2f\x00") # end of track
        f2.seek(0)
        f2_content = f2.read()
        f.write(len(f2_content).to_bytes(4, byteorder='big'))
        f.write(f2_content)

# F Major Scale with Pitch Wheel, use another player if it does not sound like a major scale
export("ACEFHJLM.mid", b"ACEFHJLM", [random.randint(-2, 2) for _ in range(8)])
export("flag.mid", flag, mix)
export("flag_no_pitch_wheel.mid", flag)