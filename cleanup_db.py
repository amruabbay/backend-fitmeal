import sqlite3

DB_NAME = "skripsi_diet.db"

def hapus_duplikat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("--- MEMULAI PEMBERSIHAN DATABASE ---")
    
    # 1. Cek jumlah data sebelum dihapus
    cursor.execute("SELECT COUNT(*) FROM food_cache")
    awal = cursor.fetchone()[0]
    print(f"Total data awal: {awal}")
    
    # 2. Hapus Duplikat
    # Logika: Hapus semua row yang ID-nya BUKAN ID terkecil dari grup nama_makanan yang sama.
    # Artinya: Jika ada 3 'Nasi Goreng', simpan yang pertama masuk, hapus sisanya.
    query = '''
    DELETE FROM food_cache
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM food_cache
        GROUP BY nama_makanan
    )
    '''
    cursor.execute(query)
    baris_dihapus = cursor.rowcount
    
    # 3. Cek jumlah data setelah dihapus
    cursor.execute("SELECT COUNT(*) FROM food_cache")
    akhir = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    print(f"Data dihapus: {baris_dihapus}")
    print(f"Total data akhir: {akhir}")
    print("--- PEMBERSIHAN SELESAI ---")

if __name__ == "__main__":
    hapus_duplikat()