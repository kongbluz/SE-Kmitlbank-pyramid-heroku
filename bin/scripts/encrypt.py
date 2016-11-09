import bcrypt

def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')

def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)

def encode_ba(accountid):
    temp = accountid + 5495100000
    return str(temp)

def decode_ba(accountid):
    temp = int(accountid) - 5495100000
    return temp
