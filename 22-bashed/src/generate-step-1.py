import hashlib
import random
import itertools
from collections import defaultdict
from rich.progress import track
import secrets
import sys

# generate a set of (l, n, h) such that hashlib.sha1(flag[l:l+n]).hexdigest()[1:2] == h can uniquely determine the flag

# ngram_candidates[n, h] = a list of m's such that len(m) == n and hash(m) = h
ngram_candidates = defaultdict(list)
for n in range(1, 3+1):
    for m in track(itertools.product(range(128), repeat=n), total=128**n):
        m_ = bytes(m)
        h = hashlib.sha1(m_).hexdigest()[1:2]
        ngram_candidates[n, h].append(m)

def is_unique(information):
    # sanity check: is union {l, l+1, ..., l+n-1} = {0, 1, ..., lf-1}
    if set([]).union(*list(range(l, l+n) for l, n, _ in information)) != set(range(lf)): return False, None

    # flag_candidates[i] = the possible values for flag[i]
    flag_candidates = [set(range(128)) for i in range(lf)]

    # first pass: filter the candidates with n=1
    for l, n, h in information:
        if n != 1: continue
        flag_candidates[l] = flag_candidates[l] & set([candidate[0] for candidate in ngram_candidates[1, h]])
    
    changed = True
    while changed:
        print('.', end='')
        sys.stdout.flush()
        changed = False

        for l, n, h in information:
            if n == 1: continue
        
            # we are unable to filter out anything...
            if min(len(flag_candidates[l+i]) for i in range(n)) == 128: continue

            out = set(itertools.product(*flag_candidates[l:l+n])) & set(ngram_candidates[n, h])
            for i in range(n):
                new_flag_candidate = flag_candidates[l+i] & set([subout[i] for subout in out])
                if new_flag_candidate != flag_candidates[l+i]: changed = True

                flag_candidates[l+i] = new_flag_candidate
    print('')

    print(f'{sorted(map(len, flag_candidates)), sum(map(len, flag_candidates)) = }')
    if max(map(len, flag_candidates)) > 1: return False, list(map(len, flag_candidates))

    flag = bytes(candidate for candidate, in flag_candidates)
    print(f'{flag = }')

    return True, None


candidates = []
for l, n in itertools.product(range(lf), [1, 2, 3]):
    if l + n > lf: continue
    h = hashlib.sha1(flag[l:l+n]).hexdigest()[1:2] # we are picking the second character from sha1
    candidates.append((l, n, h))

assert is_unique(candidates), 'not unique even if full'

selected = []
while True:
    ok, reference = is_unique(selected)
    if ok: break
    while True:
        id = secrets.randbelow(len(candidates))
        if candidates[id] in selected: continue
        l, n, _ = candidates[id]
        # this is a useless information -- this does not reduce the search space
        if reference is not None and all(reference[l+i] == 1 for i in range(n)): continue
        break

    selected.append(candidates[id])
    print(f'{len(selected), selected = }')
