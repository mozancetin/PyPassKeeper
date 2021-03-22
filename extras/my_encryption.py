def Encrypt(msg, key=10):

    msg = str(msg)
    encryption = ""
    for i in msg:
        encryption += chr(int(ord(i)) + int(key))
    return encryption

def Decrypt(msg, key=10):

    msg = str(msg)
    decryption = ""
    for i in msg:
        decryption += chr(int(ord(i)) - int(key))
    return decryption