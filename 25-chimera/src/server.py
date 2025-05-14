import socket
import time
import sys

# Usage: python3 server.py {PORT}

lport = int(sys.argv[1])
rhost = "127.0.0.1".replace(".", ",")
rport = 9000

server = socket.socket()
server.bind(('0.0.0.0', lport))
server.listen()
print(f"Listening on 0.0.0.0 {lport}")

while True:
    client, address = server.accept()
    print(f"Connection received on {address[0]} {address[1]}")

    client.send(b'220 a\n')
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(b'331 a\n')
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(b'230 a\n')
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(b'200 a\n')
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(b'550 a\n')
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(f'227 aa ({rhost},{rport//256},{rport%256})\n'.encode()) # By default php uses EPSV which we can only specify port, so we send 227 twice to let php fallback to PASV
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(f'227 aa ({rhost},{rport//256},{rport%256})\n'.encode())
    print(client.recv(20).decode().strip())
    time.sleep(1)
    client.send(b'150 ok\n')
    client.close()