from pwn import *

def main():
    r = remote('localhost', 28121)

    r.recvuntil(b'p = ')
    p = int(r.recvline().decode())

    r.recvuntil(b'q = ')
    q = int(r.recvline().decode())

    r.recvuntil(b'g = ')
    g = int(r.recvline().decode())

    r.recvuntil(b'y = ')
    y = int(r.recvline().decode())

    r.sendlineafter(b'r = ', str(1).encode())
    r.sendlineafter(b's = ', str(q).encode())

    r.interactive()

if __name__ == '__main__':
    main()