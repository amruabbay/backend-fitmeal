import requests
import base64

# --- ISI KUNCI ANDA DI SINI ---
CLIENT_ID = '3539cf685adc4153b5d9b5fa48cbe582'
CLIENT_SECRET = '2f111c0b7f8c4eb393148ec5f543c610'

# URL FatSecret
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL = "https://platform.fatsecret.com/rest/server.api"

def get_access_token():
    """Fungsi untuk minta 'Tiket Masuk' (Token) ke FatSecret"""
    # Gabungkan ID:Secret lalu di-encode
    cred = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_cred = base64.b64encode(cred.encode()).decode()
    
    headers = {'Authorization': f'Basic {encoded_cred}'}
    data = {'grant_type': 'client_credentials', 'scope': 'basic'}
    
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Gagal dapat token:", response.text)
        return None

def cari_makanan(keyword, token):
    """Fungsi mencari makanan pakai Token tadi"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'method': 'foods.search',
        'search_expression': keyword,
        'format': 'json',
        'region': 'ID', # Region Indonesia
        'max_results': 3
    }
    
    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error API:", response.text)
        return None

# --- EKSEKUSI PROGRAM ---
print("1. Sedang meminta Token Akses...")
token = get_access_token()

# ... (Kode atas tetap sama) ...

if token:
    print("   -> Token berhasil didapatkan!")
    
    print("\n2. Mencari 'Nasi Goreng'...")
    hasil = cari_makanan("Nasi Goreng", token)
    
    # --- BAGIAN INI YANG DIUBAH UNTUK DEBUGGING ---
    print("\n[DEBUG - ISI MENTAH DARI FATSECRET]:")
    print(hasil)  # Kita cetak semua isinya ke layar
    print("---------------------------------------")

    if hasil and 'foods' in hasil and 'food' in hasil['foods']:
        # Cek apakah hasilnya list (banyak) atau dict (cuma 1)
        data_makanan = hasil['foods']['food']
        
        # Jika cuma 1 hasil, FatSecret kadang mengembalikannya bukan sebagai list
        if isinstance(data_makanan, dict):
             data_makanan = [data_makanan]

        makanan_pertama = data_makanan[0]
        print(f"\n[HASIL DITEMUKAN]")
        print(f"Nama: {makanan_pertama['food_name']}")
        print(f"ID: {makanan_pertama['food_id']}")
        print(f"Deskripsi: {makanan_pertama['food_description']}")
    else:
        print("\nFORMAT DATA TIDAK SESUAI.")
        print("Coba cek pesan error di output Debug di atas.")