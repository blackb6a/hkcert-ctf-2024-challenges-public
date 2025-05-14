from lzma import compress
import libscrc
import itertools
import crcmod
import os
from rich.progress import track


crc64_func = crcmod.mkCrcFun(0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xffffffffffffffff, rev=True)
crc = lambda x: int.to_bytes(crc64_func(x), 8, 'little')

# Test

payload = os.urandom(16)
assert compress(payload, preset=9)[-28:-20] == crc(payload)

# ========

c = bytes.fromhex('3c977d3e7c4516cd39da90976982fa2d61d7cac9a9560e4ae9cf53ac57ad0e450c5826f0b64dfe03987a78a8cb1014e21bab2083ef8bd002ac3c9f1530b081c179d85df7dd77f39b0bf5e19735b4e98c638f816f9843a7b0c9fec4e36f8d09524cd326f8b8aace39b229470e789889ba12404ad7ff7aa0dbad8496158eb88d1a952d751a8fcc5f9b0a6864be6e651f25e6b97e71474e4dee43fe8191b2ce12a8975814ba8a35763b551e6df8737b672b5aae3049f110a3f64f4537495c0a0c381253e36505d95fac4b451279013210606eea9b95f726130afbda2de4f006b47039d143884e446a46f179c93536cb826b079ec4e284682af5da45bc82c608ca06557359e4b63e0eee9e87a525a326356abc1daea625438df404c40e672b720feba46a66c599f5f6e4bdc219a8e11a2320fc9c62820cd37cd4e8967e8573c00b29640ca312d853efba4b81e71a7adb88660997eb4088a8c1f40198fdaf723b1d1a7079f7ae0349cb8336ec50192af35ef963c4f4a46bba673cde7c092b469e26703cac3dbc6b6a91ad5e97aeeb1e9c23f42832938df320f45a320d58337344b5208aa005be22b092311311a8e772fe073373bf36bc1a9e86f26bf6608585b34ddf4052e9d09eb8c66a49dfa39092ab389e6ee23d1b07198c884c22e20cd581f6bfd494aeb6a4d514584f8cbf18fece96d3e2459f4a27b9a27179abff1f1ea4e85cd940f84976ce48f43c78fd163035995bc62584e5c68d4215f0459ba4f9bcd0d565c1c0680033852bfb3ec7094293156b9fb05ab640b6f19c4f7c5f0fed7052794414845695bb38873b352af5c6d726bf53a57dde9d4c76187850b70e8f887ca63e2f9b6fe2e92c1f6545fca9a36eaa1ab0ef5a07411d9289257f43945511b66cf7908892dd317d8983d7e20a4eb3203e2ac564c900d8a34c8ef90da6720d63787266dca68873747748d4ce1beb2c3e3b2e32d82107f4ed1450d8168b28ba1745be98fa421ee3a6f3d175a05deaddba586d77140debca26be3fbc09a699027a6afc181e72c9e5e796c4b07c97c7e6a6722fc1b92a45f233f7144615e78e4235ec1af5154c1f6a7dfb71d036bd91e9ff7c28c3cc2f5343e26cc77f40c37ac7e34bdeedfddc2472640dc9ad1726805a30d23db88a9556f52598f68cc2583a88e801fa859eaa5030e883756aabaa513056d343f8b8d3f80b170e5a1f17d584d91c694093b9aab7434804889820395948d0678ea316894c053b70ec11635de08b8d56def9309fb9466d8d75c902e69b0a55e7cf48364e64c47de5ed9abc4eaf19b59846f2706626711369b9b78222d73a88bc7e40e19ffea7772d4a042213df6fcc77c63fa7f309156ea6')
cs = [c[i:i+8] for i in range(0, len(c), 8)]
hs = [int.from_bytes(c, 'little') for c in cs]

visited = []
flag = b'hkcert'

# arrr it is shuffled...
for i, j in itertools.permutations(range(len(cs)), r=2):
    if crc(cs[i] + b'hkcert\xff\xff') != cs[j]: continue
    visited.extend((i, j))

LB, RB = 25, 23
assert LB+RB == 48

ls = [crc64_func(b'\0'*8 + (x<<RB).to_bytes(6, 'big') + b'\0'*2) for x in track(range(2**LB))]
rs = [crc64_func(b'\0'*8 + (x<< 0).to_bytes(6, 'big') + b'\0'*2) for x in track(range(2**RB))]

lhs = {}
for x in track(range(2**LB)):
    h1 = ls[x]
    lhs[h1] = x

print()

for k in range(2, len(cs)):
    print(f'[ ] {k+1}/{len(cs)}')
    i = visited[-1]

    h0 = crc64_func(cs[i] + b'\0'*6 + b'\xff\xff')

    for j in track(range(len(cs))):
        if j in visited: continue

        h3 = hs[j] # h0^h1^h2^h3 = 0

        # rhs
        for y in range(2**RB):
            h2 = rs[y]
            x = lhs.get(h0^h2^h3)
            if x is None: continue
            flag += ((x<<RB) | y).to_bytes(6, 'big')
            visited.append(j)
            break

        if len(visited) != k: break

    print(flag)




# https://tukaani.org/xz/xz-file-format.txt

'''
compress(b'testtesttesttest', preset=9)

    |  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
----+------------------------------------------------
000 | fd .7 .z .X .Z 00 00 04 e6 d6 b4 .F
    |                                     02 00 .! 01
010 | 1c 00 00 00 10 cf .X cc
    |                         e0 00 0f 00 0a .] 00 .:
020 | 19 .J ce .( ea a4 .P 00 00 00 00 00 00<.c 1c .J
030 | b5 .r d1 0a a1>00 01 .& 10 .k .& ef
    |                                     fe 1f b6 f3
040 | .} 01 00 00 00 04 .Y .Z

== 1. Stream Header ==

== 1.1. Header magic bytes ==
Bytes [0x0, 0x6): fd .7 .z .X .Z 00 

== 1.2. Stream flags ==
Bytes [0x6, 0x8): 00 04

== 1.3. CRC32 ==
Bytes [0x8, 0xc); binascii.crc32(b'\x00\x04') == 0x46b4d6e6
 e6 d6 b4 .F

== 2. Block ==

== 2.1. Block header ==

== 2.1.1. Block header size ==
Bytes [0xc, 0xd): 02

== 2.1.2. Block flags ==
Bytes [0xd, 0xe): 00

== 2.1.3. List of filter flags ==

== 2.1.3.1. Filter 0 flags ==
Bytes [0xe, 0x11): .! 01 1c

== 2.1.4. Header padding ==
Bytes [0x11, 0x14): 00 00 00

== 2.1.5. CRC32 ==
Bytes [0x14, 0x18); binascii.crc32(b'\x02\x00!\x01\x1c\x00\x00\x00') == 0xcc58cf10
 10 cf .X cc

== 2.2. Compressed data ==



== 2.3. Block padding ==

== 2.4. Check ==

== 3. Index ==

== 4. Stream Footer ==

== 4.1. CRC32 ==
Bytes [0x3c, 0x40): fe 1f b6 f3

== 4.2. Backward size ==
Bytes [0x40, 0x44): .} 01 00 00 (381)

== 4.3. Stream flags ==
Bytes [0x44, 0x46): 00 04

== 4.4. Footer magic bytes ==
Bytes [0x46, 0x48): .Y .Z
'''


# b'hkcert24{tw0_crc32s_n4m3ly_zl1b_4nd_b1n45ci1_bu7_n0_CRC64_lul}\x00\x00\x00\x00y\x95R\xe7\xc9\xa2h\x11\xb1;\x1e\xe2\x16\x1f\x99\x17\xd2Eu\xaa\x04\xbb\x02\x9fKL1\xda\xcf\xb3\xb2\x9c\xa7\xf6\x92\xc3eu\xd0R\t\x12O>hN\x9a\xf47\xd4\xd4\x90\x15}\x0ey\xce\x1dF\xd4/\xf5M\x95\x1a\x88\xef4\xecC\x83\x8d\x17\xbd\x0cJ\xd91\xf6\xf4h(2A\xe9\xc2u\x17{<\x83y\xc0\x1fK\xe4\x81\xce\x98\x13\x04\x12\xcb\x17\xd4\x9cH\xdcw\x89\xf7E<p6\xc7\x9b\xcaq\xce|\xfd\xdaTwW\xbc\x847\x91K(\xba\xb3\x83i^C0zv\x80\' U\xe9+<?\x82\xb0\tY%\x0c\x93\xc5\x94\x88L\xed\xd6S\xcd\x99\xc1_8\x81\xbb\xd9_KU\xcfY\x7f\x13\xb6\xd5\x8d+\x8e\xe9\x96\x04\x7f\xcd\x89\x9b\xd4\xef"\x1a0\xc5\x1c\x03\x82_2^@\xf8\x14ZB\xacS\xfc\x88\xaeg\xa6\x98\x03;\xf8\xfc\x1f\x06\xb8\xd2\x9cm?\xf8r\xb77\xef\xe7\x0f\n\xda;\x12\xdd\x88\xd3\x7f\to\xb6\x86uN=\xf5s\xbb\x8d4.Q\xf3\xb6\xfd\x9a\xd9Qf",\xd9b\xa3.\xb2\x92\xe1\xb6\x91\xc7\xbdr\xdb\xc7g\xb2B\xf5x\xdew\xc0F\xf5\xa5\x8c(\x03\xd0>\x8caCmf>\x90\xa1\x8b\x8bB\x0fn\x05\x8e\xb0Ec,\xba7\x88\xb9\xbf\xfcE\xa2\xf49\x03\x7f\x07\x11\x85\x9cC\xd7Y?SW\xa2Z\xd5U\'5\xb3\x10\xf4\xac\x9cd}\x8b\x06"\x7fS\'\x8ase\x8aoZ6\x10B\xeeI\xc8\x84VPB\xb76\x85\x83H\x94}\x8e\x01\xa6uU\x8a\x1b\x19\xbc\xec}O>8\xe7D\x95\xb0\xa1\xef\xbaC\xed\xbc\xde\xd5\xe9\xe7/\xdb$j\xbaA\x81\xa8\x0e,r\xc9\xb3w\x95\x04ix\xd9\x04\x80\xf7\x9ay\xf9I\xc0\x98\x90\xfb\x7f\xa0\x9b\xea\xa5n\x08\xbb\xc0\xa1\xd2E6d\x9e*G\x06\xee}\x01\xe8\x992u,\xac[\x9d&\xfc~\xd1\xe4Rm`\xfe\x86\xdaF7NT\x94\xe0\xfd\x8c\xc3\x92\x97\x85\xa1 \xb9\x0ba\xc6r\xee\xbb\xc0V\x85~\xc1\x86\x02\xeb\x08\xd9\xab\xba\xd7\xee\xbcN\x01\xf6\xf8\x93\x86\x84?\x04p\x18\xad\xf7S\xe0\xc0\xcf@\x14I0\x84\xd6\x94\x15\xfb\x9e\x06e\xe1s\xdaG%=\x17\xed\xcfz p\xc8\x85L\xa3\xe4\x015\xfd\x1fxk\x94\xad\x9e\xcd\xb9\xcc\x8a4\xee\xa9\xd9\x83\xbb\x0f\x11\xed\xba\x86?<l\xe7\xd2\x89x\xd2\x1aZ7;?\xb2\x9b-\x1c!\xc1\xda\xe4\x8a\x93\xe5\xa6`\xc8\x130AUUV*\xbdE\xce\xf4\x0e\xdeh>{\xcf\x90\xc3\'\xdfB\x97\x19\xfd\xcb\x9e-\x94\x82\xdf\xec{\xd2\x1bbx0f\x1d\xab\x19\xbe\xe1\x02\xaa'
# running time: 3h 50m
