import requests
from requests_oauthlib import OAuth1

# --- ISI DENGAN KEY ANDA (PASTIKAN TIDAK ADA SPASI DI AWAL/AKHIR) ---
FS_KEY = "3539cf685adc4153b5d9b5fa48cbe582"
FS_SECRET = "2f111c0b7f8c4eb393148ec5f543c610"

def test_connection():
    url = "https://platform.fatsecret.com/rest/server.api"
    
    # Setup OAuth 1.0
    auth = OAuth1(FS_KEY, FS_SECRET, signature_type='query')
    
    # Parameter sederhana (Cari 'Apple')
    params = {
        "method": "foods.search",
        "search_expression": "Apple",
        "format": "json",
        "max_results": 1
    }
    
    print("--- MULAI TES KONEKSI ---")
    try:
        response = requests.get(url, params=params, auth=auth)
        
        print(f"Status Code: {response.status_code}")
        print("Respon Mentah dari Server:")
        print(response.text) # <--- INI YANG KITA BUTUHKAN
        
    except Exception as e:
        print(f"Error Koneksi Internet: {e}")

if __name__ == "__main__":
    test_connection()