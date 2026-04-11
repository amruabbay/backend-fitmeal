import sqlite3

DB_NAME = "skripsi_diet.db"

def seed_database():
    print("Memulai Data Seeding (Backup Profesional)...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Daftar Menu Populer yang WAJIB ADA saat Demo Sidang
    # (Supaya kalau API error, menu ini tetap muncul saat dicari)
    backup_data = [
        # --- FAST FOOD (KFC/MCD/BURGER KING) ---
        (9001, 'KFC Original Chicken (1 potong)', 'Hewani', 320, 30.0, 12.0, 18.0),
        (9002, 'KFC Crispy Chicken', 'Hewani', 380, 25.0, 15.0, 22.0),
        (9003, 'KFC Rice (Nasi)', 'Karbo', 180, 4.0, 35.0, 1.0),
        (9004, 'McDonalds Big Mac', 'Lainnya', 550, 25.0, 45.0, 30.0),
        (9005, 'McDonalds McFlurry Oreo', 'Lainnya', 380, 8.0, 55.0, 12.0),
        (9006, 'Burger King Whopper Jr', 'Lainnya', 310, 13.0, 27.0, 18.0),
        (9007, 'Burger King Cheeseburger', 'Lainnya', 300, 15.0, 30.0, 12.0),
        
        # --- MINUMAN KEKINIAN ---
        (9011, 'Chatime Milk Tea (Regular)', 'Lainnya', 220, 1.0, 45.0, 5.0),
        (9012, 'Chatime Hazelnut Chocolate', 'Lainnya', 280, 2.0, 50.0, 8.0),
        (9013, 'Kopi Kenangan Mantan', 'Lainnya', 180, 2.0, 30.0, 6.0),
        (9014, 'Starbucks Caramel Macchiato', 'Lainnya', 250, 8.0, 35.0, 7.0),
        
        # --- MAKANAN INDONESIA POPULER ---
        (9021, 'Nasi Padang Rendang (Lengkap)', 'Lainnya', 750, 35.0, 80.0, 30.0),
        (9022, 'Sate Ayam (10 tusuk + bumbu)', 'Hewani', 450, 30.0, 20.0, 25.0),
        (9023, 'Martabak Manis (1 potong)', 'Lainnya', 280, 4.0, 40.0, 12.0),
        (9024, 'Indomie Goreng (1 bungkus)', 'Karbo', 380, 8.0, 54.0, 14.0),
        (9025, 'Bakso Sapi (1 mangkok)', 'Lainnya', 320, 20.0, 35.0, 10.0),
    ]

    count = 0
    for item in backup_data:
        try:
            # Gunakan INSERT OR IGNORE agar tidak duplikat
            cursor.execute('''
                INSERT OR IGNORE INTO food_cache 
                (fatsecret_id, nama_makanan, deskripsi_asli, kategori, kalori, protein, karbo, lemak)
                VALUES (?, ?, 'Backup Data Seeding', ?, ?, ?, ?, ?)
            ''', (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
            count += 1
        except Exception as e:
            print(f"Error pada {item[1]}: {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ SUKSES! {count} Menu Populer berhasil ditanam ke database.")
    print("Sekarang coba cari 'KFC' atau 'Chatime' di iOS, pasti muncul (walaupun API error).")

if __name__ == "__main__":
    seed_database()