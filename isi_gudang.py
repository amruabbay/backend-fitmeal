import sqlite3
import requests
import base64
from utils import parsing_deskripsi_fatsecret

# --- KONFIGURASI API ---
CLIENT_ID = '3539cf685adc4153b5d9b5fa48cbe582'      # <--- PASTIKAN INI TERISI
CLIENT_SECRET = 'b0b90b3b73d94cdb8fbd4fd28362f563'  # <--- PASTIKAN INI TERISI

TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
API_URL = "https://platform.fatsecret.com/rest/server.api"
DB_NAME = "skripsi_diet.db"

def get_token():
    cred = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(cred.encode()).decode()
    headers = {'Authorization': f'Basic {encoded}'}
    data = {'grant_type': 'client_credentials', 'scope': 'basic'}
    try:
        resp = requests.post(TOKEN_URL, headers=headers, data=data)
        if resp.status_code == 200: return resp.json()['access_token']
    except: return None

def bersihkan_database():
    """Fungsi darurat untuk menghapus data salah"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_cache") # Hapus semua isi tabel
    conn.commit()
    conn.close()
    print("Database berhasil dikosongkan! Silakan isi ulang dengan data bersih.")

def simpan_selektif(list_makanan, kategori_manual):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"\n--- MODUS SELEKSI: Kategori '{kategori_manual}' ---")
    print("Ketik 'y' untuk simpan, 'n' untuk lewati, 'x' untuk stop.\n")
    
    jumlah_masuk = 0
    for food in list_makanan:
        nama = food['food_name']
        desc = food['food_description']
        gizi = parsing_deskripsi_fatsecret(desc)
        
        # Tampilkan ke Admin
        print(f"Calon Data: {nama}")
        print(f"   Gizi: {gizi['kalori']} kkal | P: {gizi['protein']}g | K: {gizi['karbo']}g | L: {gizi['lemak']}g")
        
        # KONFIRMASI MANUSIA
        pilihan = input("   >> Simpan? (y/n): ").lower()
        
        if pilihan == 'x':
            break
        elif pilihan == 'y':
            try:
                cursor.execute('''
                    INSERT INTO food_cache (fatsecret_id, nama_makanan, deskripsi_asli, kategori, kalori, protein, karbo, lemak)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (food['food_id'], nama, desc, kategori_manual, gizi['kalori'], gizi['protein'], gizi['karbo'], gizi['lemak']))
                jumlah_masuk += 1
                print("   [OK] Tersimpan.\n")
            except sqlite3.IntegrityError:
                print("   [!] Sudah ada di database.\n")
        else:
            print("   [-] Dilewati.\n")

    conn.commit()
    conn.close()
    print(f"Selesai! {jumlah_masuk} makanan valid tersimpan.")

if __name__ == "__main__":
    print("=== ALAT PENGISI DATABASE V2 (MANUAL SELECT) ===")
    
    # Menu Awal
    mode = input("Pilih Mode: \n1. Cari & Tambah Data \n2. HAPUS SEMUA DATA (Reset) \nJawab (1/2): ")
    
    if mode == '2':
        konfirmasi = input("Yakin mau hapus semua data 'Yam' dan sampah tadi? (y/n): ")
        if konfirmasi.lower() == 'y':
            bersihkan_database()
            
    elif mode == '1':
        token = get_token()
        if token:
            keyword = input("Cari Makanan: ")
            kategori = input("Kategori (Karbo/Hewani/Nabati/Sayur/Buah): ")
            
            headers = {'Authorization': f'Bearer {token}'}
            # Kita ambil 20 data biar pilihannya banyak
            params = {'method': 'foods.search', 'search_expression': keyword, 'format': 'json', 'region': 'ID', 'max_results': 20}
            
            resp = requests.get(API_URL, headers=headers, params=params)
            data = resp.json()
            
            # ... (kode atas) ...
           # ... (kode atas) ...
            if 'foods' in data and 'food' in data['foods']:
                hasil = data['foods']['food']
                if isinstance(hasil, dict): hasil = [hasil]
                simpan_selektif(hasil, kategori)
            
            # --- BAGIAN INI UNTUK MENANGKAP ERROR ---
            elif 'error' in data:
                print("\n[ERROR DARI FATSECRET]:")
                print(f"Code: {data['error']['code']}")
                print(f"Pesan: {data['error']['message']}")
            else:
                print("Tidak ditemukan. Isi respons aneh:")
                print(data)