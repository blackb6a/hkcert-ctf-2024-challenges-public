import itertools
from collections import defaultdict

ROUNDS = 14

# dp[a, b, c, d]
# = number of possibilities when there is a "SB", b "SR", c "ARK" and d "MC"
#   such that no MC is happening between ARK

possibilities = [x for x in itertools.product(range(ROUNDS+1), repeat=4)]
possibilities = sorted(possibilities, key=lambda u: sum(u))
print(f'{possibilities[:5]}')

# =======

dp = defaultdict(int)
dp[0, 0, 0, 0] = 1

for x1 in possibilities:
    for dx in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]:
        x2 = tuple(_x1+_dx for _x1, _dx in zip(x1, dx))
        if max(x2) > ROUNDS: continue

        #  if I have [1, 9] ARK, I cant do MC
        if 0 < x1[2] < ROUNDS and dx[3] > 0: continue

        dp[x2] += dp[x1]


print(dp[ROUNDS, ROUNDS, ROUNDS, ROUNDS])
print(12309355935372581458927646400000) # (14*4)! / (14!)^4
# 4705360871073570227520 = 40!/(10!)^4


# simulation

import random

ops = [j for _ in range(ROUNDS) for j in range(4)]
print(ops)

ok, cnt = 0, 0
while True:
    random.shuffle(ops)
    
    first = ops.index(0)
    last = 4*ROUNDS - ops[::-1].index(0)

    cnt += 1
    if ops[first:last].count(1) == 0:
        ok += 1

    if cnt % 10000 == 0:
        print(f'{ok}/{cnt} | {ok/cnt*100}%')