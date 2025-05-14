#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <linux/seccomp.h>
#include "seccomp-bpf.h"

#define BUFFER_SIZE 100

int command_pipefd[2]; // parent to child
int output_pipefd[2]; // child to parent


struct sock_filter filter[] = {
    VALIDATE_ARCHITECTURE,
    EXAMINE_SYSCALL,
    ALLOW_SYSCALL(read),
    ALLOW_SYSCALL(write),
    ALLOW_SYSCALL(exit),
    ALLOW_SYSCALL(getuid),
    ALLOW_SYSCALL(getcwd),
    ALLOW_SYSCALL(mmap),
    ALLOW_SYSCALL(mprotect),
    ALLOW_SYSCALL(clock_nanosleep),
    DISALLOW_PROCESS
};

void activate_seccomp()
{
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(struct sock_filter)),
        .filter = filter,
    };

    // Initialize seccomp filter
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
        perror("prctl");
        exit(EXIT_FAILURE);
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) < 0) {
        perror("prctl");
        exit(EXIT_FAILURE);
    }

}

void init() {              
  setvbuf(stdin, 0, 2, 0); 
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);
  alarm(60);               
}   

void show_banner(char *buffer) {
    char banner[] = "Welcome to the Black C2!\n";
    strcpy(buffer, banner);
}

void show_uid(char *buffer) {
    sprintf(buffer, "User ID: %d\n", getuid());
}

void show_pwd(char *buffer) {
    char cwd[0x100];
    sprintf(buffer, "Current working directory: %s\n", getcwd(cwd, sizeof(cwd)));
}

void echo(char *buffer) {
    read(0, buffer, 0x1000);
}

void do_exit(char *buffer) {
    char message[] = "Child Exiting...\n";
    strcpy(buffer, message);
}

int jobs() {
    char buffer[BUFFER_SIZE];
    char output_buffer[0x100];
    int output_size;
    int ret = 0;

    sleep(3);
    memset(output_buffer, '\0', 0x100);
    read(command_pipefd[0], buffer, BUFFER_SIZE);
    
    if (strncmp(buffer, "exit", 4) == 0) {
        do_exit(output_buffer);
        ret = 1;
    } else if (strncmp(buffer, "banner", 6) == 0) {
        show_banner(output_buffer);
    } else if (strncmp(buffer, "getuid", 6) == 0) {
        show_uid(output_buffer);
    } else if (strncmp(buffer, "pwd",3) == 0) {
        show_pwd(output_buffer);
    } else if (strncmp(buffer, "echo", 4) == 0) {
        echo(output_buffer);
    } else {
        printf("Invalid command\n");
    }


    // Send output
    output_size = strlen(output_buffer);
    // printf("Send output size: %d\n", output_size);
    write(output_pipefd[1], &output_size, sizeof(output_size));
    write(output_pipefd[1], output_buffer, output_size);

    
    return ret;
}

void *tasks() {
    // char buffer[BUFFER_SIZE];
    // char output_buffer[0x100];
    // int output_size;
    activate_seccomp();
    printf("[+] Child Spawned Successfully!\n");
    while (1) {
        if(jobs()){ break; };
    }
    pthread_exit(NULL);
    exit(0);
}

int main() {
    pid_t pid;

    init();
    if (pipe(command_pipefd) == -1 || pipe(output_pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {  // Child process
        pthread_t output_tid;

        //close(command_pipefd[1]);  // Close unused write end
        //close(output_pipefd[0]);
        
        pthread_create(&output_tid, NULL, tasks, NULL);
        pthread_join(output_tid, NULL);

        close(command_pipefd[0]);
    } else {  // Parent process
        char output_buffer[0x100];
        int output_size;
        int read_byte;

        printf("[+] Spawning a slave\n");
        // close(command_pipefd[0]);  // Close unused read end
        // close(output_pipefd[1]);  // Close unused read end

        while (1) {
            char command[BUFFER_SIZE];
            
            printf("[+] Enter command (banner, getuid, pwd, echo, exit): \n");

            read(0, command, BUFFER_SIZE);

            printf("[+] Waiting Child\n");
            // Send command to child
            write(command_pipefd[1], command, BUFFER_SIZE);

            // Read size;
            read(output_pipefd[0], &output_size, sizeof(output_size));
            printf("[+] Child called home, sent: %d bytes\n", output_size);
            printf("[+] Received output:\n");
            read(output_pipefd[0], output_buffer, output_size);
            write(1, output_buffer, output_size);

            puts("");
            
            if (strncmp(command, "exit", 4) == 0) {
                printf("[+] Parent Exiting\n");
                break;
            }

            memset(output_buffer, '\0', 0x100);
            memset(command, '\0', BUFFER_SIZE);

        }

        close(command_pipefd[1]);
    }

    return 0;
}