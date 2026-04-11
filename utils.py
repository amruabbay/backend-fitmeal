import re

def parsing_deskripsi_fatsecret(deskripsi):
    """
    Mengubah string deskripsi FatSecret menjadi Dictionary angka.
    Input: "Per 100g - Calories: 165kcal | Fat: 3.60g | Carbs: 0.00g | Protein: 31.00g"
    Output: {'kalori': 165.0, 'lemak': 3.6, 'karbo': 0.0, 'protein': 31.0}
    """
    
    # Nilai default jika data tidak ditemukan (biar gak error)
    data_gizi = {
        'kalori': 0.0,
        'protein': 0.0,
        'karbo': 0.0,
        'lemak': 0.0
    }
    
    try:
        # 1. Ambil Kalori (Cari angka di antara 'Calories:' dan 'kcal')
        # Pola regex: Calories:\s*([0-9\.]+)
        search_kalori = re.search(r'Calories:\s*([0-9\.]+)', deskripsi)
        if search_kalori:
            data_gizi['kalori'] = float(search_kalori.group(1))

        # 2. Ambil Protein (Cari angka setelah 'Protein:')
        search_prot = re.search(r'Protein:\s*([0-9\.]+)', deskripsi)
        if search_prot:
            data_gizi['protein'] = float(search_prot.group(1))

        # 3. Ambil Karbo (Carbs)
        search_karbo = re.search(r'Carbs:\s*([0-9\.]+)', deskripsi)
        if search_karbo:
            data_gizi['karbo'] = float(search_karbo.group(1))

        # 4. Ambil Lemak (Fat)
        search_lemak = re.search(r'Fat:\s*([0-9\.]+)', deskripsi)
        if search_lemak:
            data_gizi['lemak'] = float(search_lemak.group(1))
            
    except Exception as e:
        print(f"Error parsing: {e}")
        
    return data_gizi

# --- AREA TEST MANUAL ---
if __name__ == "__main__":
    # Ini contoh string asli dari FatSecret
    contoh_data = "Per 100g - Calories: 165kcal | Fat: 3.60g | Carbs: 0.00g | Protein: 31.00g"
    
    print("Data Asli:", contoh_data)
    hasil_bersih = parsing_deskripsi_fatsecret(contoh_data)
    
    print("\nHasil Parsing (Siap Masuk Database):")
    print(hasil_bersih)
    
    # Cek tipe data (Harus float, bukan string)
    print(f"\nTipe data Kalori: {type(hasil_bersih['kalori'])}")