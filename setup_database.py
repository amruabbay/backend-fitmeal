import sqlite3

# Nama file database
DB_NAME = "skripsi_diet.db"

def create_tables():
    # 1. Buka koneksi ke file database (kalau belum ada, otomatis dibuat)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("Sedang membuat tabel database...")

    # --- TABEL 1: USER (Menyimpan Profil & Goal) ---
    # Kita simpan TDEE dan Goal (Cutting/Bulking) di sini
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        berat_badan REAL,
        tinggi_badan REAL,
        umur INTEGER,
        gender TEXT,
        activity_level REAL,
        goal TEXT, 
        target_kalori REAL,
        target_protein REAL,
        target_karbo REAL,
        target_lemak REAL
    )
    ''')

    # --- TABEL 2: FOOD_CACHE (Gudang Makanan) ---
    # Ini tempat menyimpan hasil copy dari FatSecret
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fatsecret_id TEXT UNIQUE, 
        nama_makanan TEXT,
        deskripsi_asli TEXT,
        kategori TEXT,
        kalori REAL,
        protein REAL,
        karbo REAL,
        lemak REAL,
        porsi_gram REAL DEFAULT 100
    )
    ''')

    # --- TABEL 3: MEAL_PLANS (Hasil Rekomendasi) ---
    # Untuk menyimpan history menu yang pernah dibuat
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meal_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tanggal DATE DEFAULT CURRENT_DATE,
        waktu_makan TEXT, -- Pagi/Siang/Malam
        menu_json TEXT,   -- Daftar ID makanan disimpan sbg text JSON
        total_kalori REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()
    print(f"Berhasil! File database '{DB_NAME}' telah dibuat.")

if __name__ == "__main__":
    create_tables()