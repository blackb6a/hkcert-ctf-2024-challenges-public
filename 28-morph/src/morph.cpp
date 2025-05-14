#include <cstring>
#include <iostream>

using namespace std;

bool verify_0(string& flag) {
    if (flag[0] & flag[1] == 1) return true;
    return false;
}


void decompress(char* memory, int size, char k) {
    for (int i = 0; i < size; i++) {
        memory[i] ^= k;
    }
}

int main() {
    string flag;
    cout << "Enter serial key: " << endl;
    cin >> flag;

    // repeat this block
    decompress((char*)verify_0, 96, random);

    cout << "Take my money and flag!" << endl;
    return 0;
fail:
    cout << "Go away hacker" << endl;
    return -1;
}
