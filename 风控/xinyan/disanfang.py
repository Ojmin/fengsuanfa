import base64
from Crypto.Cipher import AES


def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes


# 加密
def encrypted_text(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器

    return str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')


# 揭秘
def text_decrypted(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器

    return str(aes.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))


from tools import generateMD5

if __name__ == '__main__':
    name ='1'
    idcard='1'
    mobile='1'
    tokenId = ''  # 密码
    appId = ''

    param =str("name="+name+','+"idcard="+idcard+','+"mobile="+mobile)
    #name=1,idcard=1,mobile=1
    print(param)
    tokenKey = generateMD5('http://api.tcredit.com/assessment/infernalProbe' + tokenId + param)
    text = 'abc123def456'  # 待加密文本
    print(encrypted_text(tokenId, text))
