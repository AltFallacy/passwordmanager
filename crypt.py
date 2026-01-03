from cryptography.fernet import Fernet

def new_key():
    key=Fernet.generate_key()
    return key
