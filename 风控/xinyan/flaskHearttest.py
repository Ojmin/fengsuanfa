import json
import time
import requests
from warningSystem import send_mail

# while True:
# resp = requests.get('https://www.risktech.top/heartBeat', params={'sign': '1'})
resp = requests.get('http://127.0.0.1:8001/heartBeat', params={'sign': '1'})
status = resp.status_code
if status == 200:
    pass
else:
    send_mail('flask 服务器炸了')
    time.sleep(1)


