import sqlite3

DB_NAME = "skripsi_diet.db"

def suntik_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Data manual (Format: ID_Palsu, Nama, Kategori, Kalori, Prot, Karbo, Lemak)
    # ID kita buat ngasal saja (999xx) biar beda sama FatSecret
    paket_darurat = [
        # --- KARBO ---
        ('99901', 'Nasi Putih (100g)', 'Karbo', 130, 2.7, 28.0, 0.3),
        ('99902', 'Nasi Merah (100g)', 'Karbo', 110, 2.8, 23.0, 0.8),
        ('99903', 'Ubi Rebus (100g)',   'Karbo', 87,  1.6, 20.0, 0.1),
        ('99904', 'Kentang Rebus (100g)','Karbo', 87,  1.9, 20.0, 0.1),
        ('99905', 'Oatmeal Masak (100g)','Karbo', 70,  2.5, 12.0, 1.4),

        # --- HEWANI (TAMBAHAN INDONESIA) ---
        ('99941', 'Dada Ayam Rebus (100g)', 'Hewani', 165, 31.0, 0.0, 3.6),
        ('99942', 'Dada Ayam Bakar (100g)', 'Hewani', 170, 30.0, 0.0, 5.0),
        ('99943', 'Telur Rebus (1 butir besar)', 'Hewani', 78, 6.3, 0.6, 5.3),
        ('99944', 'Telur Dadar (1 butir)', 'Hewani', 95, 6.5, 1.0, 7.0),
        ('99945', 'Ikan Kembung Goreng (100g)', 'Hewani', 180, 19.0, 0.0, 10.0),

        # --- NABATI ---
        ('99911', 'Tempe Goreng (50g)', 'Nabati', 100, 9.0, 4.0, 6.0),
        ('99912', 'Tahu Putih Kukus (100g)', 'Nabati', 78, 8.0, 1.9, 4.8),
        ('99913', 'Tahu Goreng (50g)', 'Nabati', 35, 3.0, 1.0, 2.5),

        # --- SAYUR ---
        ('99921', 'Sayur Bayam Bening (1 mangkok)', 'Sayur', 35, 1.0, 3.0, 0.2),
        ('99922', 'Tumis Kangkung (1 porsi)', 'Sayur', 90, 3.0, 5.0, 6.0),
        ('99923', 'Brokoli Rebus (100g)', 'Sayur', 34, 2.8, 7.0, 0.4),

        # --- BUAH ---
        ('99931', 'Pisang Ambon (1 buah)', 'Buah', 90, 1.0, 23.0, 0.3),
        ('99932', 'Apel Merah (1 buah)', 'Buah', 52, 0.3, 14.0, 0.2)
    ]

    print("Sedang menyuntikkan data darurat...")
    masuk = 0
    gagal = 0

    for data in paket_darurat:
        try:
            cursor.execute('''
                INSERT INTO food_cache (fatsecret_id, nama_makanan, deskripsi_asli, kategori, kalori, protein, karbo, lemak)
                VALUES (?, ?, 'Data Manual', ?, ?, ?, ?, ?)
            ''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
            masuk += 1
            print(f"[OK] Masuk: {data[1]}")
        except sqlite3.IntegrityError:
            print(f"[-] Sudah ada: {data[1]}")
            gagal += 1

    conn.commit()
    conn.close()
    print(f"\nSelesai! {masuk} data baru berhasil masuk.")

if __name__ == "__main__":
    suntik_data()