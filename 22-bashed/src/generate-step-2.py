import hashlib
import random
import itertools
from collections import defaultdict
from rich.progress import track
import secrets
import sys

host = 'https://c22-bashed.hkcert24.pwnable.hk'
flag = b'hkcert24{s33m1n9ly_b3g19n_b4sh_scr1p7s_c0u1d_b3_d4n93r0us_wh3n_7h3y_4r3_s3lf_m0d1fy1n9}'
instructions = 256

# ================

lf = len(flag)

charset = [
    '👂', '👃', '👄', '👅', '👆', '👇', '👈', '👉', '👊', '👋',
    '👌', '👍', '👎', '👏', '👐', '👑', '👒', '👓', '👔', '👕',
    '👖', '👗', '👘', '👙', '👚', '👛', '👜', '👝', '👞', '👟',
    '👠', '👡', '👢', '👣', '👤', '👥', '👦', '👧', '👨', '👩',
    '👪', '👫', '👬', '👭', '👮', '👯', '👰', '👱', '👲', '👳',
    '👴', '👵', '👶', '👷', '👸', '👹', '👺', '👻', '👼', '👽',
    '👾', '👿', '💀', '💁', '💂', '💃', '💄', '💅', '💆', '💇',
    '💈', '💉', '💊', '💋', '💌', '💍', '💎', '💏', '💐', '💑',
    '💒', '💓', '💔', '💕', '💖', '💗', '💘', '💙', '💚', '💛',
    '💜', '💝', '💞', '💟', '💠', '💡', '💢', '💣', '💤', '💥',
    '💦', '💧', '💨', '💩', '💪', '💫', '💬', '💭', '💮', '💯',
    '💰', '💱', '💲', '💳', '💴', '💵', '💶', '💷', '💸', '💹',
    '💺', '💻', '💼', '💽', '💾', '💿', '📀', '📁', '📂', '📃',
    '📄', '📅', '📆', '📇', '📈', '📉', '📊', '📋', '📌', '📍',
    '📎', '📏', '📐', '📑', '📒', '📓', '📔', '📕', '📖', '📗',
    '📘', '📙', '📚', '📛', '📜', '📝', '📞', '📟', '📠', '📡',
    '📢', '📣', '📤', '📥', '📦'
][:lf]
charset_size = len(charset)

# assuming the charset is at least as long as the flag length
assert len(charset) >= len(flag)

# assuming that they are consecutive in ascii values
assert list(map(ord, charset)) == list(range(
    min(map(ord, charset)), max(map(ord, charset))+1
))

# assuming that the sha1 digest is complete
assert set([hashlib.sha1(c.encode()).hexdigest()[1:2] for c in charset]) == set('0123456789abcdef')

# ================================================

while True:
    candidates = []
    for l, n in itertools.product(range(lf), [1, 2, 3]):
        if l + n > lf: continue
        candidates.append((l, n))

    _path = [(38, 1, '3'), (58, 3, '4'), (43, 2, '0'), (54, 2, '2'), (51, 2, '8'), (19, 3, 'd'), (24, 2, 'a'), (34, 2, '2'), (75, 1, 'a'), (48, 1, 'c'), (18, 3, '0'), (43, 3, '8'), (48, 3, '0'), (69, 3, '6'), (38, 3, 'd'), (75, 3, '3'), (32, 1, '4'), (82, 3, '7'), (49, 2, 'f'), (0, 2, 'f'), (40, 3, 'f'), (14, 1, '1'), (74, 1, '7'), (47, 1, '3'), (61, 1, '1'), (64, 1, '7'), (25, 1, '3'), (2, 3, '4'), (57, 1, '3'), (27, 3, '9'), (70, 3, 'e'), (41, 2, '5'), (17, 1, '5'), (63, 1, '0'), (7, 2, '1'), (57, 3, '4'), (39, 1, '4'), (53, 1, 'd'), (35, 2, '8'), (68, 1, 'b'), (43, 1, 'c'), (46, 2, 'a'), (71, 3, '5'), (28, 2, '6'), (84, 2, 'b'), (50, 3, '1'), (47, 3, 'a'), (8, 1, '0'), (5, 2, 'a'), (6, 2, 'd'), (39, 2, '1'), (33, 3, '6'), (73, 1, '7'), (26, 2, '6'), (11, 2, '4'), (84, 3, '2'), (77, 3, '2'), (2, 2, '4'), (4, 3, '9'), (58, 2, '7'), (80, 2, 'd'), (35, 3, 'c'), (78, 3, '6'), (72, 2, 'd'), (7, 3, '1'), (27, 2, '3'), (21, 1, '4'), (7, 1, 'b'), (28, 3, 'a'), (9, 2, 'd'), (30, 1, '3'), (79, 1, 'c'), (22, 3, 'c'), (54, 1, '6'), (22, 2, '3'), (42, 3, '9'), (64, 2, 'd'), (56, 1, '0'), (80, 1, '5'), (36, 3, '1'), (78, 1, '6'), (4, 2, 'd'), (67, 2, '4'), (79, 2, 'e'), (48, 2, '3'), (77, 2, 'd'), (73, 2, 'c'), (60, 2, '3'), (51, 1, 'a'), (69, 2, 'a'), (1, 3, 'e'), (8, 2, '4'), (12, 3, '9'), (3, 1, '8'), (62, 2, '7'), (50, 1, '1'), (10, 1, '7'), (44, 1, '3'), (41, 3, '4'), (68, 2, 'b'), (23, 2, '3'), (54, 3, 'f'), (60, 3, 'b'), (84, 1, '1'), (77, 1, 'b'), (26, 1, '9'), (10, 3, 'b'), (21, 3, 'd'), (49, 3, '0'), (55, 3, '7'), (68, 3, 'b'), (3, 2, '0'), (46, 1, '7'), (69, 1, 'd'), (44, 2, '8'), (0, 1, '7'), (22, 1, '5'), (59, 2, 'd'), (66, 3, '1'), (81, 3, 'b'), (26, 3, 'd'), (81, 1, 'a'), (8, 3, 'b'), (20, 3, '6'), (52, 3, '0'), (14, 3, 'f'), (1, 2, '2'), (85, 1, 'a'), (83, 1, '5'), (37, 2, '5'), (4, 1, 'd'), (33, 1, 'd'), (72, 1, '0'), (44, 3, '0'), (51, 3, 'b'), (57, 2, '7'), (59, 1, '7'), (35, 1, '1'), (25, 3, '3'), (52, 1, '7'), (18, 1, '3'), (11, 1, '7'), (29, 3, 'd'), (47, 2, '3'), (42, 2, '1'), (45, 3, '5'), (67, 3, '4'), (21, 2, '4'), (38, 2, '8'), (58, 1, 'f'), (1, 1, '3'), (12, 1, 'b'), (28, 1, '0'), (37, 1, '0'), (63, 3, '6'), (76, 2, '5'), (40, 1, '6'), (67, 1, '3'), (66, 1, '5'), (81, 2, '9'), (76, 3, '2'), (14, 2, 'b'), (30, 3, '2'), (83, 3, 'c'), (25, 2, '8'), (15, 3, 'f'), (83, 2, '4'), (24, 3, '5'), (20, 1, '7'), (55, 1, '1'), (17, 2, '9'), (30, 2, '0'), (16, 2, 'c'), (23, 3, '9'), (61, 3, 'a'), (31, 3, 'f'), (17, 3, 'a'), (13, 1, '5'), (23, 1, 'a'), (65, 3, 'c'), (74, 3, '6'), (86, 1, '2'), (0, 3, '7')]

    # label the good ones
    path = []
    for l, n, h in _path:
        while True:
            penalty = 0
            u = ord(charset[secrets.randbelow(charset_size)])
            while u % 2 == 0:
                u //= 2
                penalty += 1
            if penalty > 0: break
        path.append((l, n, h, penalty, True))

    # add 63 good ones that are impossible to reach
    total_penalty = 0
    while total_penalty < 63:
        while True:
            l, n = random.choice(candidates)
            if (l, n, 'x', 1, True) in path: continue
            if (l, n, 'x', 2, True) in path: continue
            if (l, n, 'x', 3, True) in path: continue
            if (l, n, 'x', 4, True) in path: continue
            if (l, n, 'x', 5, True) in path: continue
            if (l, n, 'x', 6, True) in path: continue
            if (l, n, 'x', 7, True) in path: continue
            break
        while True:
            penalty = 0
            u = ord(charset[secrets.randbelow(charset_size)])
            while u % 2 == 0:
                u //= 2
                penalty += 1
            if penalty > 0: break
        path.append((l, n, 'x', penalty, True))
        total_penalty += penalty
    if total_penalty > 63: continue
    
    path_length = len(path)

    # add a bunch of confusing ones
    while len(path) < instructions:
        l, n = random.choice(candidates)
        if secrets.randbelow(path_length) < len(_path):
            h = '0123456789abcdef'[secrets.randbits(4)]
        else:
            h = 'x'
        while True:
            penalty = 0
            u = ord(charset[secrets.randbelow(charset_size)])
            while u % 2 == 0:
                u //= 2
                penalty += 1
            if penalty > 0: break
        path.append((l, n, h, penalty, False))
        assert path[-1][3] > 0

    # ====


    while True:
        random.shuffle(path)
        if not path[0][3]: continue
        if not path[1][3]: continue
        break

    # print(f'{path = }')
    good_path = [(l, n, h, p) for l, n, h, p, g in path if g]
    # print(f'{good_path = }')
    good_node_indexes = [i for i in range(instructions) if path[i][4]] + [instructions]
    # print(f'{good_node_indexes = }') 
    intended_jumps = [0] + [secrets.randbelow(charset_size) for _ in range(path_length)]
    # print(f'{intended_jumps = }')
    assert len(good_node_indexes) == len(intended_jumps)

    file_if_true     = [None for _ in range(instructions)]
    file_if_false    = [None for _ in range(instructions)]
    next_instruction = [[None for _ in range(instructions)] for _ in range(charset_size)]

    # fix some instructions based on good node indexes and intended jumps
    for i in range(path_length):
        file_from, file_to = intended_jumps[i], intended_jumps[i+1]
        idx_from,  idx_to  = good_node_indexes[i], good_node_indexes[i+1]

        if good_path[i][2] != 'x':
            file_if_true[idx_from] = file_to
            file_if_false[idx_from] = secrets.randbelow(charset_size)
        else:
            file_if_false[idx_from] = file_to
            file_if_true[idx_from] = secrets.randbelow(charset_size)

        for id in range(idx_from, idx_to):
            next_instruction[file_from][id] = idx_to

    # randomly assign the remaining stuffs
    for i in range(instructions):
        if file_if_true[i] is None:
            file_if_true[i] = secrets.randbelow(charset_size)
            file_if_false[i] = secrets.randbelow(charset_size)


    for f, i in itertools.product(range(charset_size), range(instructions)):
        if next_instruction[f][i] is None:
            if secrets.randbelow(instructions) < path_length:
                next_instruction[f][i] = i+1
            else:
                next_instruction[f][i] = i+2

    for f in range(charset_size):
        next_instruction[f][0] = 1
        next_instruction[f][instructions-1] = instructions

    # shortest path = 63

    INFTY = 0x3f3f3f3f
    dp = [[[INFTY, 0] for _ in range(lf)] for _ in range(instructions+1)]

    dp[0][0] = [0, 1] # distance, count

    for i1 in range(instructions):
        for j1 in range(lf):
            if dp[i1][j1][0] == INFTY: continue

            i2 = i1+1
            while i2 < instructions and next_instruction[j1][i2-1] != i2: i2 += 1

            if path[i1][2] not in 'x':
                j2 = file_if_true[i1]
                if dp[i1][j1][0] < dp[i2][j2][0]:
                    dp[i2][j2] = [dp[i1][j1][0], dp[i1][j1][1]]
                elif dp[i1][j1][0] == dp[i2][j2][0]:
                    dp[i2][j2][1] += dp[i1][j1][1]
                # print(f'V: {(i1, j1)} {dp[i1][j1]} -> {(i2, j2)} {dp[i2][j2]}')
            if True:
                penalty = path[i1][3]
                j2 = file_if_false[i1]
                if dp[i1][j1][0]+penalty < dp[i2][j2][0]:
                    dp[i2][j2] = [dp[i1][j1][0]+penalty, dp[i1][j1][1]]
                elif dp[i1][j1][0]+penalty == dp[i2][j2][0]:
                    dp[i2][j2][1] += dp[i1][j1][1]
                # print(f'X: {(i1, j1)} {dp[i1][j1]} -> {(i2, j2)} {dp[i2][j2]}')

    u = min(dp[instructions][i][0] for i in range(lf))
    print(f'{u = }')
    # assert u <= 63
    if u != 63: continue

    v = sum(dp[instructions][i][1] for i in range(lf) if dp[instructions][i][0] == 63)
    print(f'{v = }')
    if v > 1: continue

    break

for f in range(charset_size):
    print(f'file #{f:03d}/{charset[f]}: ', end='')

    for i in range(instructions):
        u, v = file_if_true[i], file_if_false[i]
        
        u = '___' if u is None else format(u, '03d')
        v = '___' if v is None else format(v, '03d')

        x = '✅❌'[path[i][2] == 'x']
        print(f'[{x}/{u}/{v}]', end='')

        if next_instruction[f][i] is None:
            print('_', end='')
        elif next_instruction[f][i] == i+1:
            print(';', end='')
        else:
            print(' ', end='')

    print()



arg_orders = [list(range(7)) for k2 in range(charset_size)]
for k2 in range(charset_size):
    random.shuffle(arg_orders[k2])

fns = []
arguments = []
for i in range(instructions):
    u, v = file_if_true[i], file_if_false[i]
    
    u = '___' if u is None else format(u, '03d')
    v = '___' if v is None else format(v, '03d')

    x = '✅❌'[path[i][2] == 'x']

    good_idx = 0
    while ord(charset[good_idx]) % 2 != 1:
        good_idx = secrets.randbelow(charset_size)
    bad_idx = 0

    # print('..', path[i])
    while ord(charset[bad_idx]) % (2 * 2**path[i][3]) != 2**path[i][3]:
        bad_idx = secrets.randbelow(charset_size)
        # print(path[i][3], charset[bad_idx], ord(charset[bad_idx]))
    
    # print(path[i], charset[bad_idx], ord(charset[bad_idx]), '*')
    # input(f'-')

    fns.append(secrets.randbelow(charset_size))
    arguments.append([
        path[i][0],
        path[i][1],
        secrets.randbelow(charset_size-16)+16 if path[i][2] == 'x' else int(path[i][2], 16),
        file_if_true[i],
        file_if_false[i],
        good_idx,
        bad_idx,
    ])
    # print(arguments[-1])



for k in range(charset_size):
    with open(f'out/{charset[k]}.sh', 'w') as f:
        f.write(f'''
#!/bin/bash

FLAG=$1
GALF=1

if ! [[ "$FLAG" =~ ^[0-9A-Za-z_{{}}]{{{lf}}}$ ]]; then echo 💔; exit 0; fi
function 🌚() {{ echo $(printf "%d" "'$1"); }}
function 🌝() {{ echo $(printf "%x" "$1"); }}
function 🍋() {{
    u=$(echo -n ${{FLAG:$(($(🌚 $1)-$(🌚 👂))):$(($(🌚 $2)-$(🌚 👂)))}} | sha1sum);
    if [[ ${{u:1:1}} == $(🌝 $(($(🌚 $3)-$(🌚 👂)))) ]];
        then wget {host}/$4.sh -O $(basename $0) >/dev/null 2>&1; GALF=$((GALF*$(🌚 $6)));
        else wget {host}/$5.sh -O $(basename $0) >/dev/null 2>&1; GALF=$((GALF*$(🌚 $7)));
    fi;
}}
'''.strip() + '\n')

        for k2 in range(charset_size):
            args = [f'${x+1}' for x in arg_orders[k2]]
            args = ' '.join(args)
            f.write(f'function {charset[k2]}() {{ 🍋 {args}; }}\n')
        f.write('\n')

        for i in range(instructions):
            f.write(charset[fns[i]])
            f.write(' ')
            for j in range(7):
                f.write(charset[arguments[i][arg_orders[fns[i]].index(j)]])
                f.write(' ')

            assert next_instruction[k][i] is not None
            if next_instruction[k][i] == i+1:
                f.write(' \n')
            else:
                f.write('\\\n')

        f.write('\n\n')
        f.write('''if [[ "$GALF" -ne 0 ]]; then echo ❤️; else echo 💔; fi\n''')

# python3 -u generate-step-2.py; cp out/👂.sh out.sh; chmod +x out.sh
