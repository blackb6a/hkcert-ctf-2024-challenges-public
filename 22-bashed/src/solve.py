import itertools
import os
import hashlib

INFTY = 0x3f3f3f3f

def trailing_zero_bits(n):
    m = 0
    while n % 2 == 0:
        n //= 2
        m += 1
    return m

def dp(initial_file):
    cost = {(u, v): INFTY for u, v in itertools.product(range(nodes_per_file+1), files.keys())}
    src  = {(u, v): None  for u, v in itertools.product(range(nodes_per_file+1), files.keys())}

    cost[0, initial_file] = 0

    for instruction_start, file_start in itertools.product(range(nodes_per_file), files.keys()):
        if cost[instruction_start, file_start] == INFTY: continue

        # it is important that instruction_start goes slower

        left, n, target, fn_true, fn_false, _, penalty = instructions[instruction_start]

        instruction_end = instruction_start
        while instruction_end < nodes_per_file and files[file_start][instruction_end]: instruction_end += 1
        instruction_end += 1

        # if correct...
        file_end = f'{fn_true}.sh'
        #                                                                            **************** this is achievable
        if cost[instruction_start, file_start] < cost[instruction_end, file_end] and 0 <= target < 16:
            cost[instruction_end, file_end] = cost[instruction_start, file_start]
            src[instruction_end, file_end] = (instruction_start, file_start, (left, n, format(target, 'x')))

        # if incorrect...
        file_end = f'{fn_false}.sh'
        if cost[instruction_start, file_start]+penalty < cost[instruction_end, file_end]:
            cost[instruction_end, file_end] = cost[instruction_start, file_start]+penalty
            src[instruction_end, file_end] = (instruction_start, file_start, None)

    return cost, src

flags_found = []
def derive_flag(conditions):
    # sort by l+n in (l, n, t), the ending position of the characters
    conditions = sorted(conditions, key=lambda key: key[0]+key[1])

    flag_candidates = [(b'', 0)]
    while len(flag_candidates) > 0:
        # flag_prefix, id = flag_candidates.pop() # dfs
        flag_prefix, id = flag_candidates.pop(0) # bfs

        if id == len(conditions):
            if flag_prefix in flags_found: continue
            print(flag_prefix)
            flags_found.append(flag_prefix)
            continue

        # guess few bytes according to the gap
        gap = (conditions[id][0]+conditions[id][1]) - (conditions[id-1][0]+conditions[id-1][1]) if id > 0 else 1
        for guess in itertools.product(range(128), repeat=gap):
            flag = flag_prefix + bytes(guess)
            id2 = id

            ok = True
            while True:
                if id2 == len(conditions): break

                l, n, t = conditions[id2]
                if len(flag) < l+n: break

                if hashlib.sha1(flag[l:l+n]).hexdigest()[1:2] != t:
                    ok = False
                    break

                id2 += 1

            if ok: flag_candidates.append((flag, id2))

# ===

# Read the functions and instructions

functions = {}
instructions = []

with open('./out/👂.sh') as f:
    lines = f.read().split('\n')

for line in lines[15:15+87]:
    fn = line[9]
    args = [int(arg)-1 for arg in line[18:-1:3]]
    functions[fn] = args

for line in lines[103:-4]:
    params = line[:16:2]
    fn, args = params[0], params[1:]

    # the arranged args
    args = [args[functions[fn][i]] for i in range(7)]
    args[0] = ord(args[0]) - ord('👂')
    args[1] = ord(args[1]) - ord('👂')
    args[2] = ord(args[2]) - ord('👂')

    args[5] = trailing_zero_bits(ord(args[5]))
    args[6] = trailing_zero_bits(ord(args[6]))

    assert 0 <= args[0] < 87
    assert args[1] in [1, 2, 3]
    assert 0 <= args[0]+args[1] <= 87
    assert args[5] == 0

    instructions.append(args)

# Read the jumps from the files

file_ids = []
files = {}
for fn in os.listdir('./out'):
    with open(f'./out/{fn}') as f:
        lines = f.read().split('\n')
    files[fn] = [line[-1] == '\\' for line in lines[103:-4]]
    file_ids.append(fn)


# Build a graph for traversal

nodes_per_file  = len(files['👂.sh'])
number_of_files = len(files)


# costs[file_id, node_id] = minimum_cost
# src[file_id, node_id] = the node that it comes from

cost, src = dp('👂.sh')

for file in files.keys():
    if cost[nodes_per_file, file] == INFTY: continue
    
    current_instruction = nodes_per_file
    current_file = file
    
    conditions = []
    while src[current_instruction, current_file] is not None:
        next_instruction, next_file, condition = src[current_instruction, current_file]
        if condition is not None: conditions.append(condition)
        current_instruction, current_file = next_instruction, next_file

    derive_flag(conditions)