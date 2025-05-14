

flag = b"hkcert24{s3lf_m0d1fy1ng_c0d3_th0_th15_i5_n0T_A_m4lw4r3}"

fn_key = b'2ps5y\x96T\x8aj9\x90\xd6+\xa3\x07\x00\x1e)d\x92S\xb6\xf5\xc7\x8a\xeb\x7f\xfe\x8a\x81\x03\x88s\x945<\x1d(G\x15\xbd\xd2CU\xd8l\x01\xaf\xe4\xab\xa7\xdc0\xd5'

prefix = """
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <sys/mman.h>

using namespace std;
"""

output = prefix

import random

random_order = list(range(len(flag) - 1))
random.shuffle(random_order)


for i in range(len(flag)-1):
    output += f"bool verify_{random_order[i]}(string& flag) "
    output += "{"
    output += f"""
    if ((flag[{i}] ^ flag[{i+1}]) == {flag[i] ^ flag[i+1]}) return true;
    return false;
"""
    output += "}\n"

output += """
void decompress(char* memory, int size, char k) {
    for (int i = 0; i < size; i++) {
        memory[i] ^= k;
    }
}

int main() {
    string flag;
    cout << "Enter serial key: " << endl;
    cin >> flag;

    typedef bool checker_fn(string&);
"""

for i in range(0, len(flag)-1):
    output += f"    decompress((char*)verify_{i}, 86, {fn_key[i]});\n"
    output += f"    if (!verify_{i}(flag)) "
    output += """{
        goto fail;
    }

"""

output += """
    cout << "Take my money and flag!" << endl;
    return 0;
fail:
    cout << "Go away hacker" << endl;
    return -1;
}
"""

with open("output.cpp", "w") as f:
    f.write(output)
