from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()
def hash_password(password: str):
    return password_hasher.hash(password)

def verify(plain, hash):
    return password_hasher.verify(plain, hash)