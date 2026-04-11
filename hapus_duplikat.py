import sqlite3

DB_NAME = "skripsi_diet.db"

def bersihkan_duplikat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("🧹 MEMULAI PEMBERSIHAN DUPLIKAT...")
    
    # 1. Cek jumlah data sebelum dihapus
    cursor.execute("SELECT COUNT(*) FROM food_cache")
    jumlah_awal = cursor.fetchone()[0]
    print(f"   Total data saat ini: {jumlah_awal}")
    
    # 2. HAPUS DUPLIKAT (Berdasarkan Nama Makanan)
    # Logika: Simpan ID terkecil (data pertama), hapus ID lain yang namanya sama.
    query = '''
    DELETE FROM food_cache
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM food_cache
        GROUP BY nama_makanan
    )
    '''
    
    cursor.execute(query)
    jumlah_dihapus = cursor.rowcount
    conn.commit()
    
    # 3. Cek jumlah data setelah dihapus
    cursor.execute("SELECT COUNT(*) FROM food_cache")
    jumlah_akhir = cursor.fetchone()[0]
    conn.close()
    
    print("-" * 30)
    if jumlah_dihapus > 0:
        print(f"✅ SUKSES! Ditemukan dan dihapus {jumlah_dihapus} data ganda.")
    else:
        print("✅ DATABASE BERSIH! Tidak ada duplikat ditemukan.")
        
    print(f"   Sisa data unik: {jumlah_akhir}")

if __name__ == "__main__":
    bersihkan_duplikat()