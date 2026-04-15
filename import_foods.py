import pandas as pd
from sqlalchemy import create_engine

# 1. Konfigurasi Nama File
csv_filename = 'datafoods.csv'
db_filename = 'skripsi_diet.db'
table_name = 'foods'  # Ganti jika nama tabel di DB Anda berbeda, misal: 'makanan'

def run_import():
    try:
        # 2. Membaca data dari CSV
        print(f"📖 Membaca file {csv_filename}...")
        df = pd.read_csv(csv_filename)

        # 3. Pembersihan Data: Menghapus kolom 'id' dari CSV
        # Kita hapus agar database menggunakan Auto Increment miliknya sendiri
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
            print("💡 Kolom 'id' dari CSV diabaikan (menggunakan Auto Increment DB).")

        # 4. Membuat koneksi ke SQLite
        engine = create_engine(f'sqlite:///{db_filename}')

        # 5. Memasukkan data ke tabel
        # if_exists='append': Menambahkan data tanpa menghapus yang sudah ada
        # index=False: Tidak menyertakan index pandas sebagai kolom baru
        print(f"🚀 Mengirim {len(df)} data ke tabel '{table_name}'...")
        df.to_sql(table_name, con=engine, if_exists='append', index=False)

        print(f"✅ Berhasil! {len(df)} makanan baru ditambahkan ke {db_filename}.")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    run_import()