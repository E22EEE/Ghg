from config import Config
import websocket
import ssl
import os
import json
import gzip
import requests
from time import sleep
import random
import concurrent.futures

created=0
failed=0


L = '\033[1;33m' #اصفر
C = "\033[1;97m" #ابيض
B = '\033[2;36m'#سمائي
Y = '\033[1;34m' #ازرق فاتح.
C = "\033[1;97m" #ابيض
X = '\037' #ابيض
G = '\033[1;32m'
R = '\033[1;31m'

id = '5154904380'

token = '6733998812:AAE9StkHrOGyIDuSLYMXoBRa0ZJ7ee510QM'

import time 
time.sleep(5)


ch='qwertyuioplkjhgfdsazxcvbnm'
def create():
 global created
 global failed
 user=str(random.choice('qwertyuioplkjhgfdsazxcvbnm')[0])+str(''.join(random.choice(ch) for i in range(13)))
 
 tlg = f'''
 {user}
   '''
 
 #user='kdvdfejevfsheh'
 
 headers = {
     "app": "com.safeum.android",
     "host": None,
     "remoteIp": "134.209.93.111",
     "remotePort": str(8080),
     "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
     "time": "2023-04-30 12:13:32",
     "url": "wss://51.79.208.190/Auth"
 }
 
 
 data0={"action":"Register","subaction":"Desktop","locale":"en_GB","gmt":"+02","password":{"m1x":"503c73d12b354f86ff9706b2114704380876f59f1444133e62ca27b5ee8127cc","m1y":"6387ae32b7087257452ae27fc8a925ddd6ba31d955639838249c02b3de175dfc","m2":"219d1d9b049550f26a6c7b7914a44da1b5c931eff8692dbfe3127eeb1a922fcf","iv":"e38cb9e83aef6ceb60a7a71493317903","message":"0d99759f972c527722a18a74b3e0b3c6060fe1be3ad53581a7692ff67b7bb651a18cde40552972d6d0b1482e119abde6203f5ab4985940da19bb998bb73f523806ed67cc6c9dbd310fd59fedee420f32"},"magicword":{"m1x":"04eb364e4ef79f31f3e95df2a956e9c72ddc7b8ed4bf965f4cea42739dbe8a4a","m1y":"ef1608faa151cb7989b0ba7f57b39822d7b282511a77c4d7a33afe8165bdc1ab","m2":"4b4d1468bfaf01a82c574ea71c44052d3ecb7c2866a2ced102d0a1a55901c94b","iv":"b31d0165dde6b3d204263d6ea4b96789","message":"8c6ec7ce0b9108d882bb076be6e49fe2"},"magicwordhint":"0000","login":str(user),"devicename":"Xiaomi Redmi Note 8 Pro","softwareversion":"1.1.0.1380","nickname":"hvtctchnjvfxfx","os":"AND","deviceuid":"c72d110c1ae40d50","devicepushuid":"*dxT6B6Solm0:APA91bHqL8wxzlyKHckKxMDz66HmUqmxCPAVKBDrs8KcxCAjwdpxIPTCfRmeEw8Jks_q13vOSFsOVjCVhb-CkkKmTUsaiS7YOYHQS_pbH1g6P4N-jlnRzySQwGvqMP1gxRVksHiOXKKP","osversion":"and_11.0.0","id":"1734805704"}
 
 ws=websocket.create_connection("wss://51.79.208.190/Auth", header=headers, sslopt={"cert_reqs": ssl.CERT_NONE})
 ws.send(json.dumps(data0))
 result=ws.recv()
 decoded_data = gzip.decompress(result)
 #print(G+str(decoded_data))
 if '"comment":"Exists"' in str(decoded_data):
  failed+=1
 elif '"status":"Success"' in str(decoded_data):
  created+=1
  y = requests.post(f"https://api.telegram.org/bot{token}/sendmessage?chat_id={id}&text="+str(tlg))
 elif '"comment":"Retry"' in str(decoded_data):
  failed+=1
 else:
  print(decoded_data)


executor=concurrent.futures.ThreadPoolExecutor(max_workers=500)

while True:
 executor.submit(create)
 os.system('clear')
 
 print(G+'Created : '+str(created))
 print(R+'Failed : '+str(failed))
