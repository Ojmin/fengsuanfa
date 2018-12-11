import datetime
import hashlib
import json
import rsa
import base64
def xinyan(orderNo, name, idcard):
    _data = {
        'member_id ': '8000013189',
        'terminal_id': '8000013189',
        'trade_date': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'trans_id': orderNo + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'industry_type': 'B18',
        'id_no': generateMD5(idcard),
        'id_name': generateMD5(name),
        'product_type': 'QJLDLEZ',
        'versions': '1.4.0',
    }
    data_content = json.dumps(_data)


def generateMD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def rsaEncrypt(message):

    # message1 = json.dumps(message)
    with open('../key1/8000013189_pri.pem','r') as f:
        # print(f.read().replace('\r',''))
        a = f.read().replace('\r','')
        print(a.encode())
        privkey = rsa.PrivateKey.load_pkcs1(a.encode())
        message1 = base64.b64encode(message.encode('utf-8'))
    # privkey = rsa.PrivateKey.load_pkcs1(data)
    print(privkey)
    crypto = rsa.encrypt(message1, privkey)
    return crypto


if __name__ == '__main__':
    # (pub,privkey) = rsa.newkeys(1024)
    # print(privkey.save_pkcs1())
    # priv = rsa.PrivateKey.load_pkcs1(privkey.save_pkcs1())
    # print(priv)
    # print(rsa.encrypt('fdsf'.encode('utf-8'),priv))
    rsaEncrypt('fsdf')