import json

import requests as requests
from flask import Flask
from flask import request

from tools import AESCipher, tokenId, TokenKey, appId
from tools import TCApplyNeedleUrl, TCCreditNeedleUrl, TCWJNeedleUrl

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    if request.method == "POST":
        json_data = request.get_data().decode('utf-8')
        _data = json.loads(json_data)
        orderNo = _data['orderNo']
        name = _data['name']
        idcard = _data['idcard']
        mobile = _data['mobile']
        json1 = json.dumps({'name': name, 'idcard': idcard, 'mobile': mobile})
        param = str(AESCipher.encrypt(json1, tokenId.replace('-', '')), encoding="utf-8")
        parameter = ("param=%s" % (param))
        parameterXY = ("name=%s,idCard=%s,mobile=%s" % (name, idcard, mobile))
        XYTZparams = {'tokenKey': TokenKey.getTokenKey(parameterXY, TCCreditNeedleUrl), 'appId': appId, 'name': name, 'idCard': idcard,
                      'mobile': mobile}
        WJTZparams = {'tokenKey': TokenKey.getTokenKey(parameter,TCWJNeedleUrl), 'appId': appId, 'param': param}
        ANparams = {'tokenKey': TokenKey.getTokenKey(parameter,TCApplyNeedleUrl), 'appId': appId, 'param': param}
        r1 = requests.post(TCCreditNeedleUrl, XYTZparams)
        TCdata = r1.text
        print(TCdata)

        r2 = requests.post(TCWJNeedleUrl,WJTZparams)
        print(r2.text)
        rep = json.loads(r2.text)
        if rep["status"] == 0:
            data = rep["data"]
            TCdata1 = AESCipher.decode_data(data, tokenId.replace('-', ''))
            print("TCdata1解密后", TCdata1)

        r3 = requests.post(TCApplyNeedleUrl,ANparams)
        print(r3.text)
        rep = json.loads(r3.text)
        if rep["status"] == 0:
            data = rep["data"]
            TCdata2 = AESCipher.decode_data(data, tokenId.replace('-', ''))
            print("TCdata2解密后", TCdata2)


            return json.dumps(TCdata2)


if __name__ == '__main__':
    app.run()
