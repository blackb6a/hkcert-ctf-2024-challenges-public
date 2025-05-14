#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <ctype.h>
#include <string.h>
#define SIZE 100
typedef void (*void_fn)(void);

void _abort(char const * err_msg) {
    printf("%s", err_msg);
    exit(1);
}

void init() {
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);
  alarm(60);
}

int blacklist(char* s) {
    for (int i = 0; i < SIZE; i++)
        if ((char)s[i] == 0x0f || (char)s[i] == 0xcd)
            return 1;
    return 0;
}

int main() {
    int readed_len = 0;
    unsigned long rbx, rcx, rdx, rbp, rsp, rsi, rdi, r8, r9, r10, r11, r12, r13;
    char *shellcode;
    unsigned long jmp_addr = 0x13370000;

    init();

    shellcode = (char*) mmap((void *)0x13370000, SIZE, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    if ((long)shellcode == -1) _abort("mmap failed!\n");
    memset(shellcode, '\0', SIZE);

    printf("\nInput your shellcode here (max: 100): ");
    if ((readed_len = read(0, shellcode, SIZE - 1)) == 0) _abort("read failed!\n");
    if (blacklist(shellcode)) _abort("bye\n");

    mprotect(shellcode, SIZE, PROT_EXEC);
    
    asm(    
        "xor %%rax, %%rax;"
        "xor %%rbx, %%rbx;"
        "xor %%rcx, %%rcx;"
        "xor %%rdx, %%rdx;"
        "xor %%rsi, %%rsi;"
        "xor %%rdi, %%rdi;"
        "xor %%r8, %%r8;"
        "xor %%r9, %%r9;"
        "xor %%r10, %%r10;"
        "xor %%r11, %%r11;"
        "xor %%r12, %%r12;"
        "xor %%r13, %%r13;"
        "xor %%r14, %%r14;"
        "xor %%r15, %%r15;"
        "xor %%rsp, %%rsp;"
        "xorps %%xmm0, %%xmm0 \n\t"
        "xorps %%xmm1, %%xmm1 \n\t"
        "xorps %%xmm2, %%xmm2 \n\t"
        "xorps %%xmm3, %%xmm3 \n\t"
        "xorps %%xmm4, %%xmm4 \n\t"
        "xorps %%xmm5, %%xmm5 \n\t"
        "xorps %%xmm6, %%xmm6 \n\t"
        "xorps %%xmm7, %%xmm7 \n\t"
        "xorps %%xmm8, %%xmm8 \n\t"
        "xorps %%xmm9, %%xmm9 \n\t"
        "xorps %%xmm10, %%xmm10 \n\t"
        "xorps %%xmm11, %%xmm11 \n\t"
        "xorps %%xmm12, %%xmm12 \n\t"
        "xorps %%xmm13, %%xmm13 \n\t"
        "xorps %%xmm14, %%xmm14 \n\t"
        "xorps %%xmm15, %%xmm15 \n\t"
        "mov %0, %%rdi;"
        "xor %%rbp, %%rbp;"
        "jmp *%%rdi"
        :: "m"(jmp_addr)
    );
    
}

// 0x3a4740