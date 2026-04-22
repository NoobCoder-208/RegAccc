from flask import Flask, request, jsonify
import asyncio
import register
import requests

# Tắt cảnh báo
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

async def run_registration(name_prefix, region):
    try:
        # 1. Lấy phiên bản động theo vùng
        version_info = register.tudongcapnhat(region=region)
        Ob = version_info.get("latest_release_version", "1.103.1")
        Ver = version_info.get("remote_version", "1.103.1")

        # 2. Đăng ký khách
        uid, password = register.guest_register()
        
        # 3. Lấy token
        access_token, open_id = register.guest_token(uid, password)
        
        # 4. Tên tài khoản
        name = name_prefix if name_prefix else register.TaoAccName()
            
        # 5. Đăng ký chính
        await register.major_register(access_token, open_id, name, region=region, ob=Ob)
        
        # 6. Đăng nhập chính - Sửa lại tham số ở đây
        major_login_raw = await register.major_login_async(access_token, open_id, region=region, ob=Ob, ver=Ver)
        major_res = register.decode_major_login_response(major_login_raw)
        
        if not major_res.token:
            return {"status": "error", "message": "No JWT token returned from MajorLogin"}

        jwt_token = major_res.token
        account_id = major_res.account_uid
        res_region = major_res.region
        url_base = major_res.url
        
        result = {
            "status": "success",
            "uid": uid,
            "password": password,
            "name": name,
            "account_id": account_id,
            "region": res_region
        }

        if not url_base:
            result["status"] = "partial_success"
            return result

        # 7. Kích hoạt
        try:
            payload = await register.EncRypTMajoRLoGin(open_id, access_token, region=region, ver=Ver)
            login_data_raw = await register.GetLoginData(url_base, payload, jwt_token, ob=Ob)
            login_data = register.DecodeLoginData(login_data_raw)
            
            if login_data.Online_IP_Port:
                auth_token_hex = await register.xAuThSTarTuP(
                    int(account_id), jwt_token, int(major_res.timestamp), 
                    major_res.key, major_res.iv
                )
                ip, port = login_data.Online_IP_Port.split(":")
                await register.OnTcp(ip, port, auth_token_hex, "Online")
        except: pass

        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/gen', methods=['GET'])
def gen():
    count = request.args.get('count', default=1, type=int)
    name = request.args.get('name', default=None)
    region = request.args.get('region', default='vn').lower()
    
    count = max(1, min(count, 10))
    results = []
    
    # Tạo loop mới cho mỗi request Flask để tránh xung đột loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        for _ in range(count):
            res = loop.run_until_complete(run_registration(name, region))
            results.append(res)
    finally:
        loop.close()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)