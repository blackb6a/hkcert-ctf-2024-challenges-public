
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <sys/mman.h>

using namespace std;
bool verify_43(string& flag) {
    if ((flag[0] ^ flag[1]) == 3) return true;
    return false;
}
bool verify_9(string& flag) {
    if ((flag[1] ^ flag[2]) == 8) return true;
    return false;
}
bool verify_30(string& flag) {
    if ((flag[2] ^ flag[3]) == 6) return true;
    return false;
}
bool verify_24(string& flag) {
    if ((flag[3] ^ flag[4]) == 23) return true;
    return false;
}
bool verify_42(string& flag) {
    if ((flag[4] ^ flag[5]) == 6) return true;
    return false;
}
bool verify_35(string& flag) {
    if ((flag[5] ^ flag[6]) == 70) return true;
    return false;
}
bool verify_22(string& flag) {
    if ((flag[6] ^ flag[7]) == 6) return true;
    return false;
}
bool verify_10(string& flag) {
    if ((flag[7] ^ flag[8]) == 79) return true;
    return false;
}
bool verify_28(string& flag) {
    if ((flag[8] ^ flag[9]) == 8) return true;
    return false;
}
bool verify_44(string& flag) {
    if ((flag[9] ^ flag[10]) == 64) return true;
    return false;
}
bool verify_20(string& flag) {
    if ((flag[10] ^ flag[11]) == 95) return true;
    return false;
}
bool verify_2(string& flag) {
    if ((flag[11] ^ flag[12]) == 10) return true;
    return false;
}
bool verify_5(string& flag) {
    if ((flag[12] ^ flag[13]) == 57) return true;
    return false;
}
bool verify_27(string& flag) {
    if ((flag[13] ^ flag[14]) == 50) return true;
    return false;
}
bool verify_1(string& flag) {
    if ((flag[14] ^ flag[15]) == 93) return true;
    return false;
}
bool verify_38(string& flag) {
    if ((flag[15] ^ flag[16]) == 84) return true;
    return false;
}
bool verify_52(string& flag) {
    if ((flag[16] ^ flag[17]) == 85) return true;
    return false;
}
bool verify_40(string& flag) {
    if ((flag[17] ^ flag[18]) == 87) return true;
    return false;
}
bool verify_32(string& flag) {
    if ((flag[18] ^ flag[19]) == 31) return true;
    return false;
}
bool verify_17(string& flag) {
    if ((flag[19] ^ flag[20]) == 72) return true;
    return false;
}
bool verify_31(string& flag) {
    if ((flag[20] ^ flag[21]) == 95) return true;
    return false;
}
bool verify_7(string& flag) {
    if ((flag[21] ^ flag[22]) == 9) return true;
    return false;
}
bool verify_11(string& flag) {
    if ((flag[22] ^ flag[23]) == 56) return true;
    return false;
}
bool verify_25(string& flag) {
    if ((flag[23] ^ flag[24]) == 60) return true;
    return false;
}
bool verify_49(string& flag) {
    if ((flag[24] ^ flag[25]) == 83) return true;
    return false;
}
bool verify_36(string& flag) {
    if ((flag[25] ^ flag[26]) == 84) return true;
    return false;
}
bool verify_8(string& flag) {
    if ((flag[26] ^ flag[27]) == 87) return true;
    return false;
}
bool verify_47(string& flag) {
    if ((flag[27] ^ flag[28]) == 108) return true;
    return false;
}
bool verify_41(string& flag) {
    if ((flag[28] ^ flag[29]) == 43) return true;
    return false;
}
bool verify_15(string& flag) {
    if ((flag[29] ^ flag[30]) == 28) return true;
    return false;
}
bool verify_39(string& flag) {
    if ((flag[30] ^ flag[31]) == 88) return true;
    return false;
}
bool verify_45(string& flag) {
    if ((flag[31] ^ flag[32]) == 111) return true;
    return false;
}
bool verify_51(string& flag) {
    if ((flag[32] ^ flag[33]) == 43) return true;
    return false;
}
bool verify_46(string& flag) {
    if ((flag[33] ^ flag[34]) == 28) return true;
    return false;
}
bool verify_53(string& flag) {
    if ((flag[34] ^ flag[35]) == 89) return true;
    return false;
}
bool verify_26(string& flag) {
    if ((flag[35] ^ flag[36]) == 4) return true;
    return false;
}
bool verify_50(string& flag) {
    if ((flag[36] ^ flag[37]) == 106) return true;
    return false;
}
bool verify_6(string& flag) {
    if ((flag[37] ^ flag[38]) == 54) return true;
    return false;
}
bool verify_23(string& flag) {
    if ((flag[38] ^ flag[39]) == 92) return true;
    return false;
}
bool verify_19(string& flag) {
    if ((flag[39] ^ flag[40]) == 106) return true;
    return false;
}
bool verify_14(string& flag) {
    if ((flag[40] ^ flag[41]) == 49) return true;
    return false;
}
bool verify_29(string& flag) {
    if ((flag[41] ^ flag[42]) == 94) return true;
    return false;
}
bool verify_4(string& flag) {
    if ((flag[42] ^ flag[43]) == 100) return true;
    return false;
}
bool verify_48(string& flag) {
    if ((flag[43] ^ flag[44]) == 11) return true;
    return false;
}
bool verify_16(string& flag) {
    if ((flag[44] ^ flag[45]) == 30) return true;
    return false;
}
bool verify_13(string& flag) {
    if ((flag[45] ^ flag[46]) == 30) return true;
    return false;
}
bool verify_21(string& flag) {
    if ((flag[46] ^ flag[47]) == 50) return true;
    return false;
}
bool verify_33(string& flag) {
    if ((flag[47] ^ flag[48]) == 89) return true;
    return false;
}
bool verify_0(string& flag) {
    if ((flag[48] ^ flag[49]) == 88) return true;
    return false;
}
bool verify_12(string& flag) {
    if ((flag[49] ^ flag[50]) == 27) return true;
    return false;
}
bool verify_37(string& flag) {
    if ((flag[50] ^ flag[51]) == 67) return true;
    return false;
}
bool verify_3(string& flag) {
    if ((flag[51] ^ flag[52]) == 70) return true;
    return false;
}
bool verify_34(string& flag) {
    if ((flag[52] ^ flag[53]) == 65) return true;
    return false;
}
bool verify_18(string& flag) {
    if ((flag[53] ^ flag[54]) == 78) return true;
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

    typedef bool checker_fn(string&);
    decompress((char*)verify_0, 86, 50);
    if (!verify_0(flag)) {
        goto fail;
    }

    decompress((char*)verify_1, 86, 112);
    if (!verify_1(flag)) {
        goto fail;
    }

    decompress((char*)verify_2, 86, 115);
    if (!verify_2(flag)) {
        goto fail;
    }

    decompress((char*)verify_3, 86, 53);
    if (!verify_3(flag)) {
        goto fail;
    }

    decompress((char*)verify_4, 86, 121);
    if (!verify_4(flag)) {
        goto fail;
    }

    decompress((char*)verify_5, 86, 150);
    if (!verify_5(flag)) {
        goto fail;
    }

    decompress((char*)verify_6, 86, 84);
    if (!verify_6(flag)) {
        goto fail;
    }

    decompress((char*)verify_7, 86, 138);
    if (!verify_7(flag)) {
        goto fail;
    }

    decompress((char*)verify_8, 86, 106);
    if (!verify_8(flag)) {
        goto fail;
    }

    decompress((char*)verify_9, 86, 57);
    if (!verify_9(flag)) {
        goto fail;
    }

    decompress((char*)verify_10, 86, 144);
    if (!verify_10(flag)) {
        goto fail;
    }

    decompress((char*)verify_11, 86, 214);
    if (!verify_11(flag)) {
        goto fail;
    }

    decompress((char*)verify_12, 86, 43);
    if (!verify_12(flag)) {
        goto fail;
    }

    decompress((char*)verify_13, 86, 163);
    if (!verify_13(flag)) {
        goto fail;
    }

    decompress((char*)verify_14, 86, 7);
    if (!verify_14(flag)) {
        goto fail;
    }

    decompress((char*)verify_15, 86, 0);
    if (!verify_15(flag)) {
        goto fail;
    }

    decompress((char*)verify_16, 86, 30);
    if (!verify_16(flag)) {
        goto fail;
    }

    decompress((char*)verify_17, 86, 41);
    if (!verify_17(flag)) {
        goto fail;
    }

    decompress((char*)verify_18, 86, 100);
    if (!verify_18(flag)) {
        goto fail;
    }

    decompress((char*)verify_19, 86, 146);
    if (!verify_19(flag)) {
        goto fail;
    }

    decompress((char*)verify_20, 86, 83);
    if (!verify_20(flag)) {
        goto fail;
    }

    decompress((char*)verify_21, 86, 182);
    if (!verify_21(flag)) {
        goto fail;
    }

    decompress((char*)verify_22, 86, 245);
    if (!verify_22(flag)) {
        goto fail;
    }

    decompress((char*)verify_23, 86, 199);
    if (!verify_23(flag)) {
        goto fail;
    }

    decompress((char*)verify_24, 86, 138);
    if (!verify_24(flag)) {
        goto fail;
    }

    decompress((char*)verify_25, 86, 235);
    if (!verify_25(flag)) {
        goto fail;
    }

    decompress((char*)verify_26, 86, 127);
    if (!verify_26(flag)) {
        goto fail;
    }

    decompress((char*)verify_27, 86, 254);
    if (!verify_27(flag)) {
        goto fail;
    }

    decompress((char*)verify_28, 86, 138);
    if (!verify_28(flag)) {
        goto fail;
    }

    decompress((char*)verify_29, 86, 129);
    if (!verify_29(flag)) {
        goto fail;
    }

    decompress((char*)verify_30, 86, 3);
    if (!verify_30(flag)) {
        goto fail;
    }

    decompress((char*)verify_31, 86, 136);
    if (!verify_31(flag)) {
        goto fail;
    }

    decompress((char*)verify_32, 86, 115);
    if (!verify_32(flag)) {
        goto fail;
    }

    decompress((char*)verify_33, 86, 148);
    if (!verify_33(flag)) {
        goto fail;
    }

    decompress((char*)verify_34, 86, 53);
    if (!verify_34(flag)) {
        goto fail;
    }

    decompress((char*)verify_35, 86, 60);
    if (!verify_35(flag)) {
        goto fail;
    }

    decompress((char*)verify_36, 86, 29);
    if (!verify_36(flag)) {
        goto fail;
    }

    decompress((char*)verify_37, 86, 40);
    if (!verify_37(flag)) {
        goto fail;
    }

    decompress((char*)verify_38, 86, 71);
    if (!verify_38(flag)) {
        goto fail;
    }

    decompress((char*)verify_39, 86, 21);
    if (!verify_39(flag)) {
        goto fail;
    }

    decompress((char*)verify_40, 86, 189);
    if (!verify_40(flag)) {
        goto fail;
    }

    decompress((char*)verify_41, 86, 210);
    if (!verify_41(flag)) {
        goto fail;
    }

    decompress((char*)verify_42, 86, 67);
    if (!verify_42(flag)) {
        goto fail;
    }

    decompress((char*)verify_43, 86, 85);
    if (!verify_43(flag)) {
        goto fail;
    }

    decompress((char*)verify_44, 86, 216);
    if (!verify_44(flag)) {
        goto fail;
    }

    decompress((char*)verify_45, 86, 108);
    if (!verify_45(flag)) {
        goto fail;
    }

    decompress((char*)verify_46, 86, 1);
    if (!verify_46(flag)) {
        goto fail;
    }

    decompress((char*)verify_47, 86, 175);
    if (!verify_47(flag)) {
        goto fail;
    }

    decompress((char*)verify_48, 86, 228);
    if (!verify_48(flag)) {
        goto fail;
    }

    decompress((char*)verify_49, 86, 171);
    if (!verify_49(flag)) {
        goto fail;
    }

    decompress((char*)verify_50, 86, 167);
    if (!verify_50(flag)) {
        goto fail;
    }

    decompress((char*)verify_51, 86, 220);
    if (!verify_51(flag)) {
        goto fail;
    }

    decompress((char*)verify_52, 86, 48);
    if (!verify_52(flag)) {
        goto fail;
    }

    decompress((char*)verify_53, 86, 213);
    if (!verify_53(flag)) {
        goto fail;
    }


    cout << "Take my money and flag!" << endl;
    return 0;
fail:
    cout << "Go away hacker" << endl;
    return -1;
}
