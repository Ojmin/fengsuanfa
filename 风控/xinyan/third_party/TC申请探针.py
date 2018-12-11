import requests
import hashlib
import xlrd
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

'''
描述: 以天创api的无间探针作为示例, 具体接口请根据贵公司所购买接口的接口文档的相关参数进行修改
作者：宾毅
日期: 2018年08月24号
'''
# 接口地址，具体接口参见接口文档，每个接口有不同的url地址
url = "http://api.tcredit.com/assessment/radar"
# 登录客户管理中心可查看获取appId和tokenId, 客户管理中心地址:http://api.tcredit.com/
tokenId = "08daa8d0ba2d42ceac8d6a1d083d15af"
appId = "2bcb35ec8dff46868cd8b82857f9c014"


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
    def getTokenKey(parameter):
        spkey = parameter.split(',')
        spkey.sort()
        delimiter = ','
        joinkey = delimiter.join(spkey)
        print(joinkey)
        md5 = hashlib.md5()
        md5.update((url + tokenId + joinkey).encode('utf-8'))
        tokenkey = md5.hexdigest()
        return tokenkey


if __name__ == "__main__":
    # 所需入参，请参照不同接口文档根据入参不同编写，注意参数的大小写
    name = "李奇斌"
    idcard = "620522199305123338"
    mobile = "18260166225"

    json = json.dumps({'name': name, 'idcard': idcard, 'mobile': mobile})
    param = str(AESCipher.encrypt(json, tokenId.replace('-', '')), encoding="utf-8")
    parameter = ("param=%s" % (param))
    # print(parameter)
    # param = aaa981f98b0db65ddbe4445dfdad3d9738b9d3022896c8fa18a6d021a9236c8bb44713328f5e7d81625290eab555b659341ee54c1281653d3ea6fe60e2dfad27bb8bcff145b7a1b8cd2bccf212824214856cc212fe96a2a13b6904b44fd564ba

    # parameter = ("name=%s,idCard=%s,mobile=%s" % (name, idcard, mobile))

    tokenkey = TokenKey.getTokenKey(parameter)
    params = {'tokenKey': tokenkey, 'appId': appId, 'param': param}
    print('请求参数', params)
    # 发送请求
    r = requests.post(url, params)
    result = r.json()
    print('原始出参:', result)
    # 如果status为0, 请求成功, 需将data字段的值解密
    if result["status"] == 0:
        data = result["data"]
        data = AESCipher.decode_data(data, tokenId.replace('-', ''))
        print("data解密后", data)
