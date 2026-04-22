import hmac,hashlib,requests,json,time,random,string,base64,asyncio,ssl,re,MajorLogin_pb2,IpServer_pb2,MajorRegister_pb2
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

HEX_KEY="2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
RegisterKey=bytes.fromhex(HEX_KEY)
REGION="VN"
region_normal="vn"

RegisterGuest="https://100067.connect.garena.com/api/v2/oauth/guest:register"
FindToken="https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
MajorRegister="https://loginbp.ggpolarbear.com/MajorRegister"
MajorLogin="https://loginbp.ggpolarbear.com/MajorLogin"

def AuToUdT(package):
 I=requests.get(f"https://play.google.com/store/apps/%s"%package)
 I=re.search(r'\[\[\["(\d+\.\d+\.\d+)"\]\]',I.text)
 if I:return I.group(1)
 return None

def tudongcapnhat(ver:str=AuToUdT("details?id=com.dts.freefireth")):
 if not ver:ver=AuToUdT("details?id=com.dts.freefireth")
 I="https://bdversion.ggbluefox.com/live/ver.php{}"
 II="?version=%s&lang=vi&device=android&region=VN"%ver
 res=requests.get(I.format(II))
 return res.json()
obmoi=tudongcapnhat()
Ob=obmoi["latest_release_version"]
Ver=obmoi["remote_version"]

def debug_print(step,data):
 pass

def TaoMkGuest():
 return ''.join(random.choice('0123456789ABCDEF') for _ in range(64))

def TaoAccName():
 characters="⁰¹²³⁴⁵⁶⁷⁸⁹"
 name='Obi乂BNC'+''.join(random.choice(characters) for _ in range(5))
 return name

def E_AEs(pc):
 Z=bytes.fromhex(pc)
 key=bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
 iv=bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
 cipher=AES.new(key,AES.MODE_CBC,iv)
 ciphertext=cipher.encrypt(pad(Z,AES.block_size))
 return ciphertext

async def EnC_Vr(N):
 if N<0:
  return b''
 H=[]
 while True:
  BesTo=N&0x7F
  N>>=7
  if N:
   BesTo|=0x80
  H.append(BesTo)
  if not N:
   break
 return bytes(H)

async def CrEaTe_VarianT(field_number,value):
 field_header=(field_number<<3)|0
 return await EnC_Vr(field_header)+await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number,value):
 field_header=(field_number<<3)|2
 encoded_value=value.encode() if isinstance(value,str) else value
 return await EnC_Vr(field_header)+await EnC_Vr(len(encoded_value))+encoded_value

async def CrEaTe_ProTo(fields):
 packet=bytearray()
 for field,value in fields.items():
  if isinstance(value,dict):
   nested_packet=await CrEaTe_ProTo(value)
   packet.extend(await CrEaTe_LenGTh(field,nested_packet))
  elif isinstance(value,int):
   packet.extend(await CrEaTe_VarianT(field,value))
  elif isinstance(value,str) or isinstance(value,bytes):
   packet.extend(await CrEaTe_LenGTh(field,value))
 return packet

async def EnC_PacKeT(hex_str,key,iv):
 cipher=AES.new(key,AES.MODE_CBC,iv)
 encrypted=cipher.encrypt(pad(bytes.fromhex(hex_str),AES.block_size))
 return encrypted.hex()

async def DecodE_HeX(num):
 h=hex(num)[2:]
 if len(h)==1:
  return "0"+h
 return h

async def GeneRaTePk(pk_hex,header,key,iv):
 pk_enc=await EnC_PacKeT(pk_hex,key,iv)
 length=len(pk_enc)//2
 len_hex=await DecodE_HeX(length)
 if len(len_hex)==2:
  full_header=header+"000000"
 elif len(len_hex)==3:
  full_header=header+"00000"
 elif len(len_hex)==4:
  full_header=header+"0000"
 elif len(len_hex)==5:
  full_header=header+"000"
 else:
  raise Exception("Invalid packet length")
 return bytes.fromhex(full_header+len_hex+pk_enc)

async def EnC_Uid(uid,tp='Uid'):
 h=int(uid)
 e=[]
 while h:
  e.append((h&0x7F)|(0x80 if h>0x7F else 0))
  h>>=7
 if not e:
  e.append(0)
 return bytes(e).hex() if tp=='Uid' else None

async def xAuThSTarTuP(target_uid,token,timestamp,key,iv):
 uid_hex=hex(target_uid)[2:]
 uid_length=len(uid_hex)
 encrypted_timestamp=await DecodE_HeX(timestamp)
 encrypted_account_token=token.encode().hex()
 encrypted_packet=await EnC_PacKeT(encrypted_account_token,key,iv)
 encrypted_packet_length=hex(len(encrypted_packet)//2)[2:]
 if uid_length==9:
  headers='0000000'
 elif uid_length==8:
  headers='00000000'
 elif uid_length==10:
  headers='000000'
 elif uid_length==7:
  headers='000000000'
 else:
  headers='0000000'
 return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def EncRypTMajoRLoGin(open_id,access_token):
 major_login=MajorRegister_pb2.MajorLogin()
 major_login.event_time=str(datetime.now())[:-7]
 major_login.game_name="free fire"
 major_login.platform_id=0x4
 major_login.client_version=Ver
 major_login.system_software="Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
 major_login.system_hardware="Handheld"
 major_login.telecom_operator="Verizon"
 major_login.network_type="WIFI"
 major_login.screen_width=1920
 major_login.screen_height=1080
 major_login.screen_dpi="280"
 major_login.processor_details="ARM64 FP ASIMD AES VMH | 2865 | 4"
 major_login.memory=3003
 major_login.gpu_renderer="Adreno (TM) 640"
 major_login.gpu_version="OpenGL ES 3.1 v1.46"
 major_login.unique_device_id="Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
 major_login.client_ip="223.191.51.89"
 major_login.language=region_normal 
 major_login.open_id=open_id
 major_login.open_id_type="4"
 major_login.device_type="Handheld"
 major_login.memory_available.version=55
 major_login.memory_available.hidden_value=81
 major_login.access_token=access_token
 major_login.platform_sdk_id=0x1
 major_login.network_operator_a="Verizon"
 major_login.network_type_a="WIFI"
 major_login.client_using_version="7428b253defc164018c604a1ebbfebdf"
 major_login.external_storage_total=36235
 major_login.external_storage_available=31335
 major_login.internal_storage_total=2519
 major_login.internal_storage_available=703
 major_login.game_disk_storage_available=25010
 major_login.game_disk_storage_total=26628
 major_login.external_sdcard_avail_storage=32992
 major_login.external_sdcard_total_storage=36235
 major_login.login_by=0x3
 major_login.library_path="/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
 major_login.reg_avatar=0x1
 major_login.library_token="5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
 major_login.channel_type=0x3
 major_login.cpu_type=0x2
 major_login.cpu_architecture="64"
 major_login.client_version_code="2019118695"
 major_login.graphics_api="OpenGLES2"
 major_login.supported_astc_bitset=16383
 major_login.login_open_id_type=0x4
 major_login.analytics_detail=b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
 major_login.loading_time=13564
 major_login.release_channel="android"
 major_login.extra_info="KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
 major_login.android_engine_init_flag=110009
 major_login.if_push=0x1
 major_login.is_vpn=0x1
 major_login.origin_platform_type="4"
 major_login.primary_platform_type="4"
 serialized=major_login.SerializeToString()
 key=b'Yg&tc%DEuh6%Zc^8'
 iv=b'6oyZDr22E3ychjM%'
 cipher=AES.new(key,AES.MODE_CBC,iv)
 encrypted=cipher.encrypt(pad(serialized,AES.block_size))
 return encrypted

async def major_login_async(access_token,open_id):
 encrypted_payload=await EncRypTMajoRLoGin(open_id,access_token) 
 headers={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":"loginbp.ggpolarbear.com","ReleaseVersion":Ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
 resp=requests.post(MajorLogin,headers=headers,data=encrypted_payload,verify=False,timeout=30)
 if resp.status_code!=200:
  raise Exception(f"MajorLogin failed: HTTP {resp.status_code} - {resp.text}")
 return resp.content

def decode_major_login_response(raw_bytes):
 res=MajorLogin_pb2.MajorLoginRes()
 res.ParseFromString(raw_bytes)
 return res

async def GetLoginData(base_url,payload,jwt_token):
 url=f"{base_url}/GetLoginData"
 headers={"Accept-Encoding":"gzip","Authorization":f"Bearer {jwt_token}","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":base_url.replace("https://",""),"ReleaseVersion":Ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
 resp=requests.post(url,headers=headers,data=payload,verify=False,timeout=30)
 if resp.status_code!=200:
  raise Exception(f"GetLoginData failed: HTTP {resp.status_code} - {resp.text}")
 return resp.content

def DecodeLoginData(raw_bytes):
 data=IpServer_pb2.GetLoginData()
 data.ParseFromString(raw_bytes)
 return data

async def OnTcp(ip,port,auth_token_hex,name,duration=3):
 try:
  reader,writer=await asyncio.open_connection(ip,int(port),ssl=False)
  auth_bytes=bytes.fromhex(auth_token_hex)
  writer.write(auth_bytes)
  await writer.drain()
  await asyncio.sleep(duration)
  writer.close()
  await writer.wait_closed()
  return True
 except Exception as e:
  return False

def guest_register():
 password=TaoMkGuest()
 payload={"app_id":100067,"client_type":2,"password":password,"source":2}
 body_json=json.dumps(payload,separators=(',',':'))
 signature=hmac.new(RegisterKey,body_json.encode(),hashlib.sha256).hexdigest()
 headers={"User-Agent":"GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)","Authorization":f"Signature {signature}","Content-Type":"application/json; charset=utf-8","Accept":"application/json","Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
 resp=requests.post(RegisterGuest,headers=headers,data=body_json,timeout=30,verify=False)
 if resp.status_code!=200:
  raise Exception(f"Register failed: HTTP {resp.status_code}")
 data=resp.json()
 if data.get("code")!=0:
  raise Exception(f"Register error: {data}")
 uid=data['data']['uid']
 return uid,password

def guest_token(uid,password):
 payload={"client_id":100067,"client_secret":HEX_KEY,"client_type":2,"password":password,"response_type":"token","uid":uid}
 body_json=json.dumps(payload,separators=(',',':'))
 signature=hmac.new(RegisterKey,body_json.encode(),hashlib.sha256).hexdigest()
 headers={"User-Agent":"GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)","Authorization":f"Signature {signature}","Content-Type":"application/json; charset=utf-8","Accept":"application/json","Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
 resp=requests.post(FindToken,headers=headers,data=body_json,timeout=30,verify=False)
 if resp.status_code!=200:
  raise Exception(f"Token failed: HTTP {resp.status_code}")
 data=resp.json()
 if data.get("code")!=0:
  raise Exception(f"Token error: {data}")
 access_token=data['data']['access_token']
 open_id=data['data']['open_id']
 return access_token,open_id

async def major_register(access_token,open_id,name):
 keystream=[0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
 encoded_open_id=""
 for i,ch in enumerate(open_id):
  encoded_open_id+=chr(ord(ch)^keystream[i%len(keystream)])
 field14=encoded_open_id.encode('latin1')
 payload_fields={1:name,2:access_token,3:open_id,5:102000007,6:4,7:1,13:1,14:field14,15:region_normal,16:1,17:1}
 proto_bytes=await CrEaTe_ProTo(payload_fields) 
 encrypted_payload=E_AEs(bytes(proto_bytes).hex())
 headers={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":"loginbp.ggpolarbear.com","ReleaseVersion":Ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4."}
 resp=requests.post(MajorRegister,headers=headers,data=encrypted_payload,verify=False,timeout=30)
 if resp.status_code!=200:
  raise Exception(f"MajorRegister failed: HTTP {resp.status_code}")
 return True

async def main_async():
 try:
  uid,password=guest_register()
  access_token,open_id=guest_token(uid,password)
  name=TaoAccName()
  await major_register(access_token,open_id,name)
  major_login_raw=await major_login_async(access_token,open_id)
  major_res=decode_major_login_response(major_login_raw)
  jwt_token=major_res.token
  region=major_res.region
  account_id=major_res.account_uid
  key=major_res.key
  iv=major_res.iv
  timestamp=major_res.timestamp
  url_base=major_res.url
  payload=await EncRypTMajoRLoGin(open_id,access_token)
  login_data_raw=await GetLoginData(url_base,payload,jwt_token)
  login_data=DecodeLoginData(login_data_raw)
  online_ip_port=login_data.Online_IP_Port
  chat_ip_port=login_data.AccountIP_Port
  auth_token_hex=await xAuThSTarTuP(int(account_id),jwt_token,int(timestamp),key,iv)
  online_ip,online_port=online_ip_port.split(":")
  chat_ip,chat_port=chat_ip_port.split(":")
  online_task=OnTcp(online_ip,online_port,auth_token_hex,"Online",duration=3)
  chat_task=OnTcp(chat_ip,chat_port,auth_token_hex,"Chat",duration=3)
  await asyncio.gather(online_task,chat_task)
  print("Thanh cong ")
  print(f"tên {name}")
  print(f"region {region}")
  print(f"accid {account_id}")
  print(uid)
  print(password)
 except Exception as e:
  print(f" ")
  return 1
 return 0

def main():
 requests.packages.urllib3.disable_warnings()
 loop=asyncio.new_event_loop()
 asyncio.set_event_loop(loop)
 try:
  return loop.run_until_complete(main_async())
 finally:
  loop.close()

if __name__=="__main__":
 exit(main())