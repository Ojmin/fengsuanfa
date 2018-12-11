import hashlib
from binascii import a2b_hex, b2a_hex

from Crypto.Cipher import AES

tokenId = "08daa8d0ba2d42ceac8d6a1d083d15af"
appId = "2bcb35ec8dff46868cd8b82857f9c014"
TCApplyNeedleUrl = "http://api.tcredit.com/assessment/radar"
TCCreditNeedleUrl = "http://api.tcredit.com/integration/creditProbe01"
TCWJNeedleUrl = "http://api.tcredit.com/assessment/infernalProbe"

class AESCipher:
    # 加密
    def encrypt(text, key):
        cryptor = AES.new(a2b_hex(key), AES.MODE_ECB)
        x = AES.block_size - (len(text.encode('utf-8')) % AES.block_size)
        if x != 0:
            text = text + chr(x) * x
            t = text.encode('utf-8')
        ciphertext = cryptor.encrypt(t)
        return b2a_hex(ciphertext)

    def decode_data(data, key):
        cryptor = AES.new(a2b_hex(key), AES.MODE_ECB)
        msg = cryptor.decrypt(a2b_hex(data))
        # print(msg)
        # print(len(msg))
        # print(msg[len(msg)-1])
        paddingLen = msg[len(msg) - 1]
        return msg[0:-paddingLen].decode('utf-8')


class TokenKey:
    # 获取tokenKey
    def getTokenKey(parameter,url):
        spkey = parameter.split(',')
        spkey.sort()
        delimiter = ','
        joinkey = delimiter.join(spkey)
        print(joinkey)
        md5 = hashlib.md5()
        md5.update((url + tokenId + joinkey).encode('utf-8'))
        tokenkey = md5.hexdigest()
        return tokenkey
