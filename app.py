from flask import Flask, request, jsonify
import asyncio
import register
import requests

requests.packages.urllib3.disable_warnings()
app = Flask(__name__)

async def run_registration(name_prefix, region):
    try:
        # Lấy version
        version_info = register.tudongcapnhat(region=region)
        Ob = version_info.get("latest_release_version", "1.103.1")
        Ver = version_info.get("remote_version", "1.103.1")

        # Đăng ký & Token
        uid, password = register.guest_register()
        access_token, open_id = register.guest_token(uid, password)
        
        # Tên
        name = name_prefix if name_prefix else register.TaoAccName()
        
        # Major Register
        await register.major_register(access_token, open_id, name, region=region, ob=Ob)
        
        # Major Login
        major_login_raw = await register.major_login_async(access_token, open_id, region=region, ob=Ob, ver=Ver)
        major_res = register.decode_major_login_response(major_login_raw)
        
        if not major_res.token:
            return {"status": "error", "message": "No Token"}

        # Kích hoạt TCP (Background)
        try:
            if major_res.url:
                payload = await register.EncRypTMajoRLoGin(open_id, access_token, region, Ver)
                login_data_raw = await register.GetLoginData(major_res.url, payload, major_res.token, Ob)
                login_data = register.DecodeLoginData(login_data_raw)
                if login_data.Online_IP_Port:
                    auth = await register.xAuThSTarTuP(int(major_res.account_uid), major_res.token, int(major_res.timestamp), major_res.key, major_res.iv)
                    ip, port = login_data.Online_IP_Port.split(":")
                    asyncio.create_task(register.OnTcp(ip, port, auth))
        except: pass

        return {
            "status": "success", "uid": uid, "password": password, 
            "name": name, "account_id": major_res.account_uid, "region": major_res.region
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/gen', methods=['GET'])
def gen():
    count = max(1, min(request.args.get('count', 1, type=int), 10))
    name = request.args.get('name')
    region = request.args.get('region', 'vn')
    
    results = []
    for _ in range(count):
        # Chạy từng cái một để ổn định nhất như file gốc
        res = asyncio.run(run_registration(name, region))
        results.append(res)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
