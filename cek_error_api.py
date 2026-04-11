import requests

# --- GUNAKAN KREDENSIAL ANDA ---
CLIENT_ID = "3539cf685adc4153b5d9b5fa48cbe582"      
CLIENT_SECRET = "2f111c0b7f8c4eb393148ec5f543c610"  

def debug_fatsecret():
    print("=== 1. MENCOBA MINTA TOKEN (OAUTH 2.0) ===")
    
    auth_url = "https://oauth.fatsecret.com/connect/token"
    # Header Wajib untuk Client Credentials
    payload = {'grant_type': 'client_credentials', 'scope': 'basic'}
    
    try:
        # Request Token
        auth_resp = requests.post(auth_url, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
        
        print(f"Status Auth: {auth_resp.status_code}")
        
        if auth_resp.status_code != 200:
            print("❌ GAGAL DAPAT TOKEN!")
            print("Pesan Error Server:", auth_resp.text)
            return
            
        token = auth_resp.json().get('access_token')
        print(f"✅ Token Berhasil: {token[:10]}... (disingkat)")
        
        print("\n=== 2. MENCOBA CARI 'Indomilk' ===")
        search_url = "https://platform.fatsecret.com/rest/server.api"
        headers = {'Authorization': f'Bearer {token}'}
        
        # Skenario A: Dengan Region ID
        params_id = {
            "method": "foods.search",
            "search_expression": "Indomilk",
            "format": "json",
            "region": "ID", # Kita coba pakai filter Indonesia
            "max_results": 5
        }
        
        print(">> Mencoba search dengan region='ID'...")
        resp_id = requests.get(search_url, headers=headers, params=params_id)
        print(f"Status Search: {resp_id.status_code}")
        print("Hasil Mentah:", resp_id.text)
        
        # Skenario B: Tanpa Region (Global)
        print("\n>> Mencoba search GLOBAL (Tanpa region)...")
        params_global = {
            "method": "foods.search",
            "search_expression": "Indomilk",
            "format": "json",
            "max_results": 5
        }
        resp_global = requests.get(search_url, headers=headers, params=params_global)
        print(f"Status Search Global: {resp_global.status_code}")
        print("Hasil Mentah:", resp_global.text)

    except Exception as e:
        print("CRITICAL ERROR:", e)

if __name__ == "__main__":
    debug_fatsecret()