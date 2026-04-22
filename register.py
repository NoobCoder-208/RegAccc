import hmac,hashlib,requests,json,time,random,string,base64,asyncio,ssl,re,MajorLogin_pb2,IpServer_pb2,MajorRegister_pb2
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

HEX_KEY="2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
RegisterKey=bytes.fromhex(HEX_KEY)

RegisterGuest="https://100067.connect.garena.com/api/v2/oauth/guest:register"
FindToken="https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
MajorRegister="https://loginbp.ggpolarbear.com/MajorRegister"
MajorLogin="https://loginbp.ggpolarbear.com/MajorLogin"

def AuToUdT(package):
    try:
        I=requests.get(f"https://play.google.com/store/apps/%s"%package, timeout=10)
        I=re.search(r'\[\[\["(\d+\.\d+\.\d+)"\]\]',I.text)
        if I:return I.group(1)
    except: pass
    return "1.103.1"

def tudongcapnhat(region="VN"):
    ver=AuToUdT("details?id=com.dts.freefireth")
    I="https://bdversion.ggbluefox.com/live/ver.php?version=%s&lang=vi&device=android&region=%s"
    try:
        res=requests.get(I % (ver, region.upper()), timeout=10)
        return res.json()
    except:
        return {"latest_release_version": "1.103.1", "remote_version": "1.103.1"}

def TaoMkGuest():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(64))

def TaoAccName():
    characters="⁰¹²³⁴⁵⁶⁷⁸⁹"
    return 'CHUONG'+''.join(random.choice(characters) for _ in range(5))

def E_AEs(pc):
    Z=bytes.fromhex(pc)
    key=bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv=bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    cipher=AES.new(key,AES.MODE_CBC,iv)
    return cipher.encrypt(pad(Z,AES.block_size))

async def EnC_Vr(N):
    if N<0: return b''
    H=[]
    while True:
        BesTo=N&0x7F
        N>>=7
        if N: BesTo|=0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(field_number,value):
    return await EnC_Vr((field_number<<3)|0)+await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number,value):
    encoded_value=value.encode() if isinstance(value,str) else value
    return await EnC_Vr((field_number<<3)|2)+await EnC_Vr(len(encoded_value))+encoded_value

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
    return cipher.encrypt(pad(bytes.fromhex(hex_str),AES.block_size)).hex()

async def DecodE_HeX(num):
    h=hex(num)[2:]
    return h if len(h)>1 else "0"+h

async def xAuThSTarTuP(target_uid,token,timestamp,key,iv):
    uid_hex=hex(target_uid)[2:]
    encrypted_timestamp=await DecodE_HeX(timestamp)
    encrypted_packet=await EnC_PacKeT(token.encode().hex(),key,iv)
    encrypted_packet_length=hex(len(encrypted_packet)//2)[2:]
    headers = '0' * (11 - len(uid_hex))
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def EncRypTMajoRLoGin(open_id, access_token, region="vn", ver="1.103.1"):
    major_login=MajorRegister_pb2.MajorLogin()
    major_login.event_time=str(datetime.now())[:-7]
    major_login.game_name="free fire"
    major_login.platform_id=0x4
    major_login.client_version=ver
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
    major_login.language=region.lower() 
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
    cipher=AES.new(b'Yg&tc%DEuh6%Zc^8',AES.MODE_CBC,b'6oyZDr22E3ychjM%')
    return cipher.encrypt(pad(serialized,AES.block_size))

async def major_login_async(access_token, open_id, region="vn", ob="1.103.1", ver="1.103.1"):
    encrypted_payload=await EncRypTMajoRLoGin(open_id, access_token, region, ver) 
    headers={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":"loginbp.ggpolarbear.com","ReleaseVersion":ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
    resp=requests.post(MajorLogin,headers=headers,data=encrypted_payload,verify=False,timeout=30)
    if resp.status_code!=200: raise Exception(f"MajorLogin failed: {resp.status_code}")
    return resp.content

def decode_major_login_response(raw_bytes):
    res=MajorLogin_pb2.MajorLoginRes()
    res.ParseFromString(raw_bytes)
    return res

async def GetLoginData(base_url, payload, jwt_token, ob="1.103.1"):
    url=f"{base_url}/GetLoginData"
    headers={"Accept-Encoding":"gzip","Authorization":f"Bearer {jwt_token}","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":base_url.replace("https://",""),"ReleaseVersion":ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
    resp=requests.post(url,headers=headers,data=payload,verify=False,timeout=30)
    if resp.status_code!=200: raise Exception(f"GetLoginData failed: {resp.status_code}")
    return resp.content

def DecodeLoginData(raw_bytes):
    data=IpServer_pb2.GetLoginData()
    data.ParseFromString(raw_bytes)
    return data

async def OnTcp(ip,port,auth_token_hex,name,duration=3):
    try:
        reader,writer=await asyncio.open_connection(ip,int(port),ssl=False)
        writer.write(bytes.fromhex(auth_token_hex))
        await writer.drain()
        await asyncio.sleep(duration)
        writer.close()
        await writer.wait_closed()
        return True
    except: return False

def guest_register():
    password=TaoMkGuest()
    payload={"app_id":100067,"client_type":2,"password":password,"source":2}
    body_json=json.dumps(payload,separators=(',',':'))
    signature=hmac.new(RegisterKey,body_json.encode(),hashlib.sha256).hexdigest()
    headers={"User-Agent":"GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)","Authorization":f"Signature {signature}","Content-Type":"application/json; charset=utf-8","Accept":"application/json","Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
    resp=requests.post(RegisterGuest,headers=headers,data=body_json,timeout=30,verify=False)
    data=resp.json()
    if data.get("code")!=0: raise Exception(f"Register error: {data}")
    return data['data']['uid'], password

def guest_token(uid,password):
    payload={"client_id":100067,"client_secret":HEX_KEY,"client_type":2,"password":password,"response_type":"token","uid":uid}
    body_json=json.dumps(payload,separators=(',',':'))
    signature=hmac.new(RegisterKey,body_json.encode(),hashlib.sha256).hexdigest()
    headers={"User-Agent":"GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)","Authorization":f"Signature {signature}","Content-Type":"application/json; charset=utf-8","Accept":"application/json","Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
    resp=requests.post(FindToken,headers=headers,data=body_json,timeout=30,verify=False)
    data=resp.json()
    if data.get("code")!=0: raise Exception(f"Token error: {data}")
    return data['data']['access_token'], data['data']['open_id']

async def major_register(access_token, open_id, name, region="vn", ob="1.103.1"):
    keystream=[0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    encoded_open_id = "".join(chr(ord(ch)^keystream[i%32]) for i,ch in enumerate(open_id))
    payload_fields={1:name,2:access_token,3:open_id,5:102000007,6:4,7:1,13:1,14:encoded_open_id.encode('latin1'),15:region.lower(),16:1,17:1}
    proto_bytes=await CrEaTe_ProTo(payload_fields) 
    encrypted_payload=E_AEs(bytes(proto_bytes).hex())
    headers={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue","Host":"loginbp.ggpolarbear.com","ReleaseVersion":ob,"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)","X-GA":"v1 1","X-Unity-Version":"2018.4."}
    resp=requests.post(MajorRegister,headers=headers,data=encrypted_payload,verify=False,timeout=30)
    return resp.status_code == 200
