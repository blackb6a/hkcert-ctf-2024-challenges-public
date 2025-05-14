import numpy as np

class ShiftMatrix:
    def __init__(self, size):
        self.size = size
        self.content = np.identity(size, dtype=np.uint8)
    def __str__(self):
        return "\n".join(
            "".join(map(str, row))
            for row in self.content
        )
    def __rshift__(self, other):
        assert other < self.size
        temp = ShiftMatrix(self.size)
        temp.content = np.pad(self.content[:-other], ((other, 0), (0, 0)))
        return temp
    def __lshift__(self, other):
        assert other < self.size
        temp = ShiftMatrix(self.size)
        temp.content = np.pad(self.content[other:], ((0, other), (0, 0)))
        return temp
    def __or__(self, other):
        temp = ShiftMatrix(self.size)
        temp.content = self.content | other.content
        return temp
    def __xor__(self, other):
        temp = ShiftMatrix(self.size)
        temp.content = self.content ^ other.content
        return temp
    def __and__(self, other):
        temp = ShiftMatrix(self.size)
        temp.content = self.content & other.content
        return temp
    def __mul__(self, other):
        temp = ShiftMatrix(self.size)
        temp.content = (self.content @ other.content) & 1
        return temp
    def __pow__(self, other):
        assert other >= 0
        if other == 0:
            return ShiftMatrix(self.size)
        elif other == 1:
            temp = ShiftMatrix(self.size)
            temp.content = np.array(self.content)
            return temp
        elif other & 1:
            return self * (self ** (other - 1))
        else:
            temp = self ** (other >> 1)
            return temp * temp
    def __getitem__(self, key):
        if isinstance(key, int):
            return self[key: key+1]
        elif isinstance(key, slice):
            temp = ShiftMatrix(self.size)
            start = 0 if key.start is None else key.start
            stop = self.size if key.stop is None else key.stop
            temp.content = np.pad(self.content[key], ((self.size - (stop - start), 0), (0, 0)))
        return temp
            
def unity_seed(seed):
    values = [seed & 0xffffffff]
    for _ in range(3):
        values.append((values[-1] * 1812433253 + 1) & 0xffffffff)
    bits = []
    for value in values:
        for shift in range(31, -1, -1):
            bits.append((value >> shift) & 1)
    return np.array(bits, dtype=np.uint8)

def float32(value):
    import struct
    return struct.unpack('f', struct.pack('f', value))[0]

def unity_value(arr):
    return float32((get_int(arr[-32:]) & 0x7fffff) * float32(1 / 8388607))

def get_int(arr):
    return int("".join(map(str, arr)), 2)

unity_random = ShiftMatrix(128)
v1 = unity_random[:32]
v1 = (v1 ^ (v1 << 11))[96:]
v2 = unity_random[96:]
v3 = v1 ^ v2 ^ ((v1 ^ (v2 >> 11)) >> 8)
unity_random = (unity_random << 32) | v3

roll_map = [
    (3, "INFJ"), # 0 ~ 3
    (9, "INFP"), # 3 ~ 12
    (16, "ENFP"), # 12 ~ 28
    (5, "ENFJ"), # 28 ~ 33
    (4, "INTJ"), # 33 ~ 37
    (7, "INTP"), # 37 ~ 44
    (6, "ENTP"), # 44 ~ 50
    (4, "ENTJ"), # 50 ~ 54
    (23, "ISTJ"), # 54 ~ 77
    (28, "ISFJ"), # 77 ~ 105
    (17, "ESTJ"), # 105 ~ 122
    (25, "ESFJ"), # 122 ~ 147
    (11, "ISTP"), # 147 ~ 158
    (18, "ISFP"), # 158 ~ 176
    (8, "ESTP"), # 176 ~ 184
    (17, "ESFP"), # 184 ~ 201
]

target_result = [
    "ESFP ISTP ESFJ ISFJ ESTJ ISTP ESTP ENFP ENTJ ESTJ ISTP ISTJ ISFJ ENFJ ESFP ISFP ESTP ISFP INTP ENFP ISTJ ESFJ ENTP ISTJ ISFJ ISFJ ESFP ESFJ ENFP INTP INTP ISFJ ENFJ ISTP INFP ENFP ISTJ ISFJ ESFJ ISTP INFP ESFJ ENFP ESFP ESFP ISTP ESFJ ISTJ ENFP ISTJ",
    "ISFJ ESTP ESTJ INTJ ISTP ISFJ ESFJ ISFJ ISTJ INTP ENFP ISTP ENFJ ISTJ INFP ISFP ISFP INTJ ISFJ ESFJ ISFJ ESTJ ESFP INTP ESFJ ESFJ ISFP ISFJ ESFP INTP ISFP ENFJ ISFP ESFP ESFJ ISFJ ESFP ESFP ESTP ESTP ISTP INTP ESFJ ESFJ ENFP ESFP ISFJ ISTJ ISFP ISTP",
    "ISTJ ESFJ ISFJ INTJ ESFJ ISFP ISFJ ESFJ ESFP ISFP ESTJ ISFP ENFP ENTJ INFP ESTP ISFJ INFP ISTJ ISFP INFP ESFJ ISTJ ISTJ ISFP ISFP ESFP ESTJ ESTJ INTP ESFP ISFJ ESFJ ESFJ ISFJ ISFJ ESTJ ESFP ESTJ ISTJ ENFP ESFJ ESFP ENFJ ESFJ ESFP ESFJ ESFJ ESFP ISFP",
    "INFP ESFJ ISFJ ENFP ESFJ ISFP INFP ENTJ ESFP ESTP ESFP ESFP INFP ESTP ISTJ ESFJ ISTP INTP ISFP ESTJ ISFJ ENFP ESTP ENFJ ISFJ ISTP ESFJ ESFJ ESFJ ESFJ ESFJ ESTJ INTP ISFJ ISFP ESFP ENFJ INTP ESTP ISFJ ESFP ISFJ ISTJ ISTJ ISTP ENFP ENFP ISFP ISFJ INTP",
    "ESFJ ISFP ESFJ ISFJ ISTJ ENFJ ESTJ ESTJ ISFP ISFP ESFJ ENTP ENFP ISTJ ISTP INTJ ISTJ ISFJ ESFP ISTP ISFJ ENFJ ENFJ ISFJ INTP ESFJ ISTJ INTJ ISFJ ENTP ESFJ ESFJ ISTP ESTJ ENFP ISFJ ISFP ISFJ ESTJ ISFJ ENTP ENFP ESTJ ENFP ENFP ISFJ ESTP ISFJ ISFP INTP",
    "ESFJ ESFJ INFP ESFJ ESFP ISFJ ESTJ ESFJ ESTJ ISFJ ISFP ISFJ ISFJ INFP INFJ ENTP ESTJ ISTJ ISTP ISFJ INTJ ESTJ ISFP ISFP ESFP ISTJ ESTJ ESFJ INFP ESTP ISFJ ISFJ ESTJ ISTJ ENTJ ESFP ISTJ ESFJ ESFJ ISTJ INTJ ESTJ ENFP ESTP ISTP ISFP ISFJ ESFJ INTP ESTP"
]

def certain_bits(low, high):
    """
    return bits in common for all values between low and high
    """
    assert low <= high
    lo, hi = 0, 1
    bits = []
    while True:
        mi = (lo + hi) / 2
        if high < mi:
            bits.append(0)
            hi = mi
        elif mi <= low:
            bits.append(1)
            lo = mi
        else:
            return bits

from math import ceil

sum_roll = sum([roll[0] for roll in roll_map])
roll_bits = {}
prev_sum = 0
# unity uses 8388607 instead of 8388608 as the denominator (which means 0 to 1 inclusive)
for roll in roll_map:
    new_sum = prev_sum + roll[0]
    low = ceil(prev_sum / sum_roll * 8388607)
    high = ceil(new_sum / sum_roll * 8388607)
    # notice that a 1 in result refers to 0x7fffff (8388607 / 8388608 in float), not 0x800000
    roll_bits[roll[1]] = certain_bits(low / 8388608, (high - (new_sum != sum_roll)) / 8388608)
    prev_sum = new_sum
print("Known bits:", roll_bits)


for stage, entry in enumerate(target_result):
    parts = entry.split(" ")
    entropy = sum([len(roll_bits[part]) for part in parts])
    print(f"No. of known bits in stage {stage + 1}: {entropy} {'==' if entropy == 128 else '>' if entropy > 128 else '<'} 128")

matrix_50 = []
temp = unity_random
for _ in range(50):
    matrix_50.append(temp.content)
    temp *= unity_random

charList = "0123456789abcdefghijklmnopqrstuvwxyz"
def HashName(name):
    result = 0
    for c in name:
        result *= 36
        result += charList.index(c)
        result &= 0xffffffff
    return result

def extract_name(name):
    seed = get_int(name[:32])
    result = ""
    while seed:
        result = charList[seed % 36] + result
        seed //= 36
    return result

def get_roll_result(roll):
    sum_roll = sum([roll[0] for roll in roll_map])
    actual_roll = roll * sum_roll
    prev_sum = 0
    for roll in roll_map:
        new_sum = prev_sum + roll[0]
        if prev_sum <= actual_roll < new_sum:
            return roll[1]
        prev_sum = new_sum
    return roll_map[-1][1] # the unity inclusive

def simulate(name):
    mat = unity_random.content
    state = unity_seed(HashName(name))
    parts = []
    for i in range(50):
        state = (mat @ state) & 1
        parts.append(get_roll_result(unity_value(state)))
    return " ".join(parts)

# assert simulate("1") == target_result[0]
# assert simulate("4m") == target_result[1]
# assert simulate("on3") == target_result[2]
# assert simulate("5t4r") == target_result[3]
# assert simulate("und3r") == target_result[4]
# assert simulate("c4e1um") == target_result[5]

def test_answer(answer):
    states = []
    for offset in range(0, 128, 32):
        states.append(get_int(answer[offset:offset+32]))
        if offset > 0:
            if states[-1] != (states[-2] * 1812433253 + 1) & 0xffffffff:
                return False
    return True

try:
    0/0 # remove this line to enable sagemath
    from sage.all import *
except:
    # direct replacement of sagemath
    vector = lambda x: x
    GF = lambda x: None
    class Matrix:
        def __init__(self, _, rows):
            self.content = np.array(rows, dtype=np.uint8)
        def solve_right(self, target):
            temp = np.array(self.content)
            num_vars = len(temp)
            right = np.array(target, dtype=np.uint8)
            index = 0
            has_1 = []
            for i in range(temp.shape[1]): # each column
                init_j = None # the first row to handle later
                for j in range(index, num_vars):
                    if temp[j, i] == 1:
                        init_j = j
                        break
                if init_j is None:
                    # empty
                    continue
                has_1.append(i)
                if init_j == index:
                    init_j += 1
                else:
                    # beware of reference copy in numpy
                    temp[[index, init_j]] = temp[[init_j, index]]
                    right[[index, init_j]] = right[[init_j, index]]
                    if index == num_vars:
                        break
                for j in range(init_j, num_vars):
                    if temp[j, i] == 1:
                        temp[j] ^= temp[index]
                        right[j] ^= right[index]
                index += 1
            for i in range(index, num_vars):
                if right[i] == 1:
                    raise ValueError("No solution")
            result = np.zeros(temp.shape[1], dtype=np.uint8)
            while len(has_1):
                i = has_1.pop()
                index -= 1
                result[i] = right[index]
                for j in range(index):
                    if temp[j, i] == 1:
                        temp[j] ^= temp[index]
                        right[j] ^= right[index]
            return Mod2Tuple(result)
        def right_kernel(self):
            temp = self.content.T
            num_vars = len(temp)
            right = np.identity(num_vars, dtype=np.uint8)
            index = 0
            for i in range(temp.shape[1]): # each column
                init_j = None # the first row to handle later
                for j in range(index, num_vars):
                    if temp[j, i] == 1:
                        init_j = j
                        break
                if init_j is None:
                    # empty
                    continue
                if init_j == index:
                    init_j += 1
                else:
                    # beware of reference copy in numpy
                    temp[[index, init_j]] = temp[[init_j, index]]
                    right[[index, init_j]] = right[[init_j, index]]
                    if index == num_vars:
                        break
                for j in range(init_j, num_vars):
                    if temp[j, i] == 1:
                        temp[j] ^= temp[index]
                        right[j] ^= right[index]
                index += 1
            result = [np.zeros(num_vars, dtype=np.uint8)]
            for i in range(index, num_vars):
                new_result = []
                for entry in result:
                    new_result.append(entry)
                    new_result.append(entry ^ right[i])
                result = new_result
            return list(map(Mod2Tuple, result))
    class Mod2Tuple:
        def __init__(self, v):
            self.value = v & 1
        def __add__(self, other):
            return (self.value + other.value) & 1
        def __radd__(self, other):
            return (self.value + other) & 1

from itertools import product
from rich.progress import track
flags = []
for stage, entry in enumerate(target_result):
    print(f"Breaking Stage {stage + 1}: ")
    parts = entry.split(" ")
    entropy = sum([len(roll_bits[part]) for part in parts])
    # if entropy < 113:
    if stage < 2:
        # may use brute force for earlier stages if one does not know about the matrix way, or only figure out too few relationships
        # good luck with many options to test
        # luckily the name length is less than 6
        # still, 36 ** 5 = 60466176 though
        name_length = stage + 1
        while True:
            for name in track(product(charList, repeat=name_length)):
                if simulate(name) == entry:
                    flags.append(''.join(name))
                    print("\nAnswer:", flags[-1])
                    break
            else:
                name_length += 1
                continue
            break
    else:
        rows = []
        bits = []
        for j in range(50):
            known_bits = roll_bits[parts[j]]
            for index, bit in enumerate(known_bits):
                # 23: number of lowest bits used in unity random
                rows.append(list(matrix_50[j][128 - 23 + index]))
                bits.append(bit)
        # add known relationship in the initial state to reduce search space
        # regarding 1812433253 % 2 = 1
        # 0 1
        # 1 0
        rows.append([(i in (31, 63)) for i in range(128)])
        rows.append([(i in (63, 95)) for i in range(128)])
        rows.append([(i in (95, 127)) for i in range(128)])
        bits.extend([1, 1, 1])
        # regarding 1812433253 % 4 = 1
        # notice that the 2nd lsb also exhibits linear relationship
        # 00 01
        # 01 10
        # 10 11
        # 11 00
        rows.append([(i in (30, 31, 62)) for i in range(128)])
        rows.append([(i in (62, 63, 94)) for i in range(128)])
        rows.append([(i in (94, 95, 126)) for i in range(128)])
        bits.extend([0, 0, 0])

        # Enumerate all possible answers to see which internal state is possible from an initial seed
        mat = Matrix(GF(2), rows)
        vec = vector(bits)
        answer0 = mat.solve_right(vec)
        for dx in track(mat.right_kernel()):
            answer = answer0 + dx
            if test_answer(answer):
                flags.append(extract_name(answer))
                print("\nFound Answer:", flags[-1])
                break

print(f"Flag: hkcert24{{{'_'.join(flags)}}}")

"""
Sample Running Time:
Using Sage, 3 Extra Relations, Brute Forcing first 2 stages: about 1 minute
Using Sage, 6 Extra Relations: about 0.5 minute
Using Sage, 6 Extra Relations, Brute Forcing first 2 stages: about 7 seconds
Not Using Sage, 3 Extra Relations: about 18 seconds
Not Using Sage, 6 Extra Relations: about 5 seconds
Not Using Sage, 6 Extra Relations, Brute Forcing first 2 stages: about 2 second
"""