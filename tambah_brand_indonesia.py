"""
======================================================
🇮🇩 SEEDING PRODUK BRAND INDONESIA POPULER
======================================================
Menambahkan produk-produk makanan & minuman brand Indonesia 
yang TIDAK tersedia di FatSecret API ke database lokal.

Data nutrisi per 1 sajian (serving size tertera di kemasan).
Sumber: Label kemasan / BPOM / nutrition facts resmi.
======================================================
"""

import sqlite3

DB_NAME = "skripsi_diet.db"

# Format: (fatsecret_id, nama_makanan, kategori, kalori, protein, karbo, lemak)
# fatsecret_id menggunakan prefix 99xxxxx agar tidak bentrok dengan ID asli FatSecret

BRAND_INDONESIA = [
    # ==================================
    # 🥛 SUSU & DAIRY
    # ==================================
    # --- Indomilk ---
    (9901001, "Indomilk Full Cream UHT", "Hewani", 120, 3.0, 11.0, 7.0),
    (9901002, "Indomilk Cokelat UHT", "Hewani", 130, 3.0, 18.0, 5.0),
    (9901003, "Indomilk Stroberi UHT", "Hewani", 125, 2.8, 17.0, 4.5),
    (9901004, "Indomilk Susu Kental Manis", "Hewani", 100, 1.6, 18.0, 2.0),
    (9901005, "Indomilk Good To Go Cokelat", "Hewani", 140, 5.0, 20.0, 4.0),

    # --- Ultra Milk ---
    (9902001, "Ultra Milk Full Cream", "Hewani", 120, 4.0, 10.0, 7.0),
    (9902002, "Ultra Milk Low Fat Cokelat", "Hewani", 100, 5.0, 14.0, 2.5),
    (9902003, "Ultra Milk Low Fat Strawberry", "Hewani", 100, 5.0, 14.0, 2.5),
    (9902004, "Ultra Milk Plain", "Hewani", 110, 4.0, 10.0, 6.0),
    (9902005, "Ultra Mimi Cokelat", "Hewani", 120, 3.0, 16.0, 5.0),

    # --- Frisian Flag ---
    (9903001, "Frisian Flag Full Cream UHT", "Hewani", 130, 4.0, 11.0, 8.0),
    (9903002, "Frisian Flag Coconut Delight", "Hewani", 120, 3.0, 14.0, 6.0),
    (9903003, "Frisian Flag Low Fat Belgian Chocolate", "Hewani", 90, 5.0, 12.0, 2.0),
    (9903004, "Frisian Flag Low Fat French Vanilla", "Hewani", 90, 5.0, 12.0, 2.0),
    (9903005, "Frisian Flag Milky Cokelat", "Hewani", 110, 3.0, 16.0, 3.5),
    (9903006, "Frisian Flag Susu Kental Manis Gold", "Hewani", 110, 2.0, 20.0, 2.5),

    # --- Greenfields ---
    (9904001, "Greenfields Fresh Milk Full Cream", "Hewani", 127, 5.0, 9.0, 8.0),
    (9904002, "Greenfields Fresh Milk Choco Malt", "Hewani", 120, 4.0, 15.0, 4.5),
    (9904003, "Greenfields Yogurt Strawberry", "Hewani", 90, 4.0, 14.0, 1.5),
    (9904004, "Greenfields Yogurt Blueberry", "Hewani", 90, 4.0, 14.0, 1.5),

    # --- Cimory ---
    (9905001, "Cimory Yogurt Drink Strawberry", "Hewani", 80, 2.5, 14.0, 1.0),
    (9905002, "Cimory Yogurt Drink Blueberry", "Hewani", 80, 2.5, 14.0, 1.0),
    (9905003, "Cimory Fresh Milk Full Cream", "Hewani", 130, 5.0, 10.0, 8.0),
    (9905004, "Cimory Yogurt Squeeze Mango", "Hewani", 70, 2.0, 12.0, 1.0),

    # --- Yakult ---
    (9906001, "Yakult Original", "Hewani", 50, 0.8, 11.0, 0.1),
    (9906002, "Yakult Light", "Hewani", 30, 0.8, 6.0, 0.1),
    (9906003, "Yakult Gold", "Hewani", 55, 1.0, 12.0, 0.1),

    # --- Bear Brand ---
    (9907001, "Bear Brand Susu Steril", "Hewani", 120, 4.0, 10.0, 7.0),
    (9907002, "Bear Brand Gold White Malt", "Hewani", 140, 4.0, 17.0, 6.0),
    (9907003, "Bear Brand Gold White Tea", "Hewani", 130, 4.0, 15.0, 6.0),

    # ==================================
    # 🍞 ROTI & SEREAL
    # ==================================
    # --- Sari Roti ---
    (9910001, "Sari Roti Tawar", "Karbo", 80, 3.0, 14.0, 1.0),
    (9910002, "Sari Roti Sobek Cokelat", "Karbo", 120, 3.0, 19.0, 3.5),
    (9910003, "Sari Roti Sandwich Peanut Butter", "Karbo", 150, 4.0, 20.0, 6.0),
    (9910004, "Sari Roti Kasur Cokelat Keju", "Karbo", 130, 3.5, 18.0, 5.0),

    # --- Energen ---
    (9911001, "Energen Sereal Cokelat", "Karbo", 130, 3.0, 22.0, 3.5),
    (9911002, "Energen Sereal Vanilla", "Karbo", 130, 3.0, 22.0, 3.5),
    (9911003, "Energen Sereal Kacang Hijau", "Karbo", 130, 3.0, 22.0, 3.5),

    # --- Simba / Nestle ---
    (9912001, "Simba Sereal Choco Chips", "Karbo", 140, 2.0, 24.0, 4.0),
    (9912002, "Nestle Koko Krunch", "Karbo", 150, 2.5, 25.0, 4.0),
    (9912003, "Nestle Milo Sereal", "Karbo", 140, 3.0, 24.0, 3.0),

    # ==================================
    # 🥤 MINUMAN KEMASAN
    # ==================================
    # --- Pocari Sweat ---
    (9920001, "Pocari Sweat 350ml", "Lainnya", 66, 0.0, 16.5, 0.0),
    (9920002, "Pocari Sweat Ion Water 350ml", "Lainnya", 31, 0.0, 7.7, 0.0),

    # --- Teh Botol Sosro ---
    (9921001, "Teh Botol Sosro Original 450ml", "Lainnya", 100, 0.0, 25.0, 0.0),
    (9921002, "Teh Botol Sosro Less Sugar 450ml", "Lainnya", 60, 0.0, 15.0, 0.0),
    (9921003, "S-Tee Jasmine 318ml", "Lainnya", 77, 0.0, 19.0, 0.0),

    # --- Teh Pucuk Harum ---
    (9922001, "Teh Pucuk Harum Original 350ml", "Lainnya", 70, 0.0, 17.0, 0.0),
    (9922002, "Teh Pucuk Harum Less Sugar 350ml", "Lainnya", 45, 0.0, 11.0, 0.0),

    # --- Aqua ---
    (9923001, "Aqua Mineral Water 600ml", "Lainnya", 0, 0.0, 0.0, 0.0),
    (9923002, "Aqua Reflections 380ml", "Lainnya", 0, 0.0, 0.0, 0.0),

    # --- Minute Maid ---
    (9924001, "Minute Maid Pulpy Orange 350ml", "Buah", 105, 0.0, 26.0, 0.0),
    (9924002, "Minute Maid Nutriboost Strawberry", "Hewani", 90, 1.0, 18.0, 1.0),

    # --- Le Minerale ---
    (9925001, "Le Minerale 600ml", "Lainnya", 0, 0.0, 0.0, 0.0),

    # --- Buavita ---
    (9926001, "Buavita Guava 250ml", "Buah", 100, 0.0, 24.0, 0.0),
    (9926002, "Buavita Orange 250ml", "Buah", 100, 0.5, 24.0, 0.0),
    (9926003, "Buavita Apple 250ml", "Buah", 95, 0.0, 23.0, 0.0),

    # --- ABC ---
    (9927001, "ABC Kopi Susu 250ml", "Lainnya", 120, 2.0, 20.0, 3.5),
    (9927002, "ABC Heinz Saus Sambal 10g", "Lainnya", 8, 0.1, 1.8, 0.1),

    # ==================================
    # 🍗 PROTEIN (OLAHAN KEMASAN)
    # ==================================
    # --- So Good ---
    (9930001, "So Good Chicken Nugget (5 pcs)", "Hewani", 200, 10.0, 15.0, 11.0),
    (9930002, "So Good Chicken Stick (5 pcs)", "Hewani", 180, 8.0, 14.0, 10.0),
    (9930003, "So Good Chicken Karaage (5 pcs)", "Hewani", 190, 9.0, 13.0, 11.0),
    (9930004, "So Good Sosis Ayam (3 pcs)", "Hewani", 120, 5.0, 5.0, 8.0),

    # --- Fiesta ---
    (9931001, "Fiesta Chicken Nugget (5 pcs)", "Hewani", 210, 9.0, 16.0, 12.0),
    (9931002, "Fiesta Sosis Sapi (3 pcs)", "Hewani", 130, 5.0, 4.0, 10.0),
    (9931003, "Fiesta Chicken Katsu (3 pcs)", "Hewani", 200, 8.0, 15.0, 12.0),

    # --- Kanzler ---
    (9932001, "Kanzler Frankfurter Sapi (2 pcs)", "Hewani", 180, 7.0, 3.0, 16.0),
    (9932002, "Kanzler Bratwurst (1 pc)", "Hewani", 200, 8.0, 3.0, 18.0),
    (9932003, "Kanzler Chicken Nugget (5 pcs)", "Hewani", 190, 9.0, 14.0, 11.0),

    # ==================================
    # 🍜 MIE & MAKANAN INSTAN
    # ==================================
    # --- Indomie ---
    (9940001, "Indomie Goreng Original", "Karbo", 380, 8.0, 52.0, 15.0),
    (9940002, "Indomie Goreng Rendang", "Karbo", 390, 8.0, 53.0, 16.0),
    (9940003, "Indomie Goreng Pedas", "Karbo", 380, 7.0, 52.0, 15.0),
    (9940004, "Indomie Kuah Soto", "Karbo", 310, 7.0, 44.0, 11.0),
    (9940005, "Indomie Kuah Ayam Bawang", "Karbo", 300, 7.0, 43.0, 11.0),
    (9940006, "Indomie Kuah Kari Ayam", "Karbo", 320, 7.0, 45.0, 12.0),
    (9940007, "Indomie Hype Abis Ayam Geprek", "Karbo", 370, 7.0, 50.0, 15.0),

    # --- Mie Sedaap ---
    (9941001, "Mie Sedaap Goreng", "Karbo", 390, 7.0, 53.0, 16.0),
    (9941002, "Mie Sedaap Kuah Soto", "Karbo", 310, 7.0, 43.0, 12.0),
    (9941003, "Mie Sedaap Goreng Korean Spicy", "Karbo", 400, 7.0, 54.0, 17.0),

    # --- Pop Mie ---
    (9942001, "Pop Mie Kuah Mi Goreng", "Karbo", 250, 5.0, 34.0, 10.0),
    (9942002, "Pop Mie Kuah Ayam", "Karbo", 220, 5.0, 30.0, 9.0),
    (9942003, "Pop Mie Kuah Baso", "Karbo", 220, 5.0, 30.0, 9.0),

    # --- Sarimi ---
    (9943001, "Sarimi Isi 2 Mi Goreng", "Karbo", 370, 8.0, 50.0, 14.0),
    (9943002, "Sarimi Isi 2 Soto", "Karbo", 300, 7.0, 42.0, 11.0),
    
    # ==================================
    # 🍪 SNACK & BISKUIT
    # ==================================
    # --- Oreo ---
    (9950001, "Oreo Original (3 keping)", "Karbo", 160, 1.5, 24.0, 7.0),
    (9950002, "Oreo Thin (4 keping)", "Karbo", 140, 1.5, 21.0, 6.0),

    # --- Roma ---
    (9951001, "Roma Kelapa (3 keping)", "Karbo", 120, 1.5, 17.0, 5.0),
    (9951002, "Roma Malkist Crackers (3 keping)", "Karbo", 100, 1.5, 15.0, 4.0),

    # --- Khong Guan ---
    (9952001, "Khong Guan Malkist (3 keping)", "Karbo", 110, 2.0, 16.0, 4.0),
    (9952002, "Khong Guan Saltcheese (3 keping)", "Karbo", 100, 2.0, 14.0, 4.0),

    # --- Good Day / Luwak ---
    (9953001, "Good Day Cappuccino Sachet", "Lainnya", 100, 1.5, 17.0, 3.0),
    (9953002, "Good Day Mocacinno Sachet", "Lainnya", 100, 1.5, 16.0, 3.5),
    (9953003, "Luwak White Koffie Sachet", "Lainnya", 100, 1.0, 18.0, 2.5),
    (9953004, "Kapal Api Special Mix Sachet", "Lainnya", 90, 1.0, 16.0, 2.0),
    (9953005, "Torabika Cappuccino Sachet", "Lainnya", 110, 1.5, 18.0, 3.5),

    # --- Nabati ---
    (9954001, "Nabati Richeese (1 bungkus)", "Karbo", 130, 2.0, 16.0, 7.0),
    (9954002, "Nabati Richoco (1 bungkus)", "Karbo", 130, 2.0, 16.0, 7.0),

    # ==================================
    # 🍚 BUMBU & PELENGKAP INDONESIA
    # ==================================
    # --- Kecap & Saus ---
    (9960001, "Kecap Bango Manis 15ml", "Lainnya", 25, 0.5, 5.0, 0.0),
    (9960002, "Kecap ABC Manis 15ml", "Lainnya", 25, 0.5, 5.5, 0.0),
    (9960003, "Saus Sambal ABC 10g", "Lainnya", 8, 0.1, 1.8, 0.1),
    (9960004, "Saus Sambal Indofood 10g", "Lainnya", 7, 0.1, 1.5, 0.1),

    # --- Bumbu Masak ---
    (9961001, "Royco Kaldu Ayam (1 sachet)", "Lainnya", 10, 0.3, 1.5, 0.2),
    (9961002, "Masako Rasa Ayam (1 sachet)", "Lainnya", 10, 0.3, 1.5, 0.2),

    # ==================================
    # 🥚 TELUR & TAHU TEMPE (Penting!)
    # ==================================
    (9970001, "Telur Ayam Rebus (1 butir)", "Hewani", 70, 6.0, 0.5, 5.0),
    (9970002, "Telur Ayam Ceplok (1 butir)", "Hewani", 90, 6.0, 0.5, 7.0),
    (9970003, "Telur Puyuh Rebus (5 butir)", "Hewani", 70, 5.5, 0.5, 5.0),
    (9970004, "Tahu Putih (1 potong besar)", "Nabati", 80, 9.0, 2.0, 4.5),
    (9970005, "Tahu Sumedang Goreng (3 potong)", "Nabati", 150, 8.0, 5.0, 11.0),
    (9970006, "Tempe Goreng (3 potong)", "Nabati", 190, 12.0, 8.0, 13.0),
    (9970007, "Tempe Rebus/Kukus (100g)", "Nabati", 150, 14.0, 8.0, 7.5),
    (9970008, "Tempe Bacem (3 potong)", "Nabati", 200, 12.0, 15.0, 10.0),
    (9970009, "Oncom Goreng (100g)", "Nabati", 170, 11.0, 12.0, 8.0),
]


def tambah_brand():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    berhasil = 0
    gagal_duplikat = 0
    
    for produk in BRAND_INDONESIA:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO food_cache 
                (fatsecret_id, nama_makanan, kategori, kalori, protein, karbo, lemak)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', produk)
            
            if cursor.rowcount > 0:
                berhasil += 1
            else:
                gagal_duplikat += 1
                
        except Exception as e:
            print(f"Error insert {produk[1]}: {e}")
    
    conn.commit()
    conn.close()
    
    print("=" * 50)
    print("🇮🇩 SEEDING BRAND INDONESIA SELESAI!")
    print("=" * 50)
    print(f"✅ Berhasil ditambahkan : {berhasil} produk")
    print(f"⏭️  Dilewati (duplikat)  : {gagal_duplikat} produk")
    print(f"📦 Total data           : {berhasil + gagal_duplikat} produk")
    print("=" * 50)


if __name__ == "__main__":
    tambah_brand()
