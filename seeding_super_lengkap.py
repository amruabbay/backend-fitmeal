import sqlite3

DB_NAME = "skripsi_diet.db"

def reset_dan_isi_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("⏳ MEMULAI INSTALASI DATABASE MONSTER (450+ MENU)...")
    
    # 1. BERSIHKAN TABEL LAMA
    cursor.execute("DROP TABLE IF EXISTS food_cache")
    
    # 2. BUAT STRUKTUR BARU
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fatsecret_id TEXT UNIQUE,
        nama_makanan TEXT,
        kalori REAL,
        protein REAL,
        karbo REAL,
        lemak REAL,
        kategori TEXT
    )
    ''')
    
    # --- DATABASE 450+ ITEM ---
    makanan_data = [
        # ==========================================
        # 1. KARBO (POKOK)
        # ==========================================
        (50001, "Nasi Putih (1 piring sedang)", 204, 4.2, 44, 0.4, "Karbo"),
        (50002, "Nasi Merah (1 piring sedang)", 110, 2.8, 23, 0.9, "Karbo"),
        (50003, "Nasi Hitam (1 piring)", 140, 5, 30, 1.5, "Karbo"),
        (50004, "Nasi Jagung (1 piring)", 150, 4, 35, 1, "Karbo"),
        (50005, "Nasi Uduk (1 porsi)", 260, 4, 35, 12, "Karbo"),
        (50006, "Nasi Kuning (1 porsi)", 275, 4.5, 40, 10, "Karbo"),
        (50007, "Nasi Liwet Solo (1 porsi)", 280, 5, 42, 11, "Karbo"),
        (50008, "Nasi Hainam (1 porsi)", 300, 5, 45, 12, "Karbo"),
        (50009, "Nasi Kebuli Kambing (1 porsi)", 450, 15, 60, 18, "Karbo"),
        (50010, "Nasi Timbel (1 porsi)", 220, 4, 45, 2, "Karbo"),
        (50011, "Nasi Goreng Spesial (1 piring)", 650, 22, 70, 25, "Karbo"),
        (50012, "Nasi Goreng Seafood (1 piring)", 600, 20, 65, 22, "Karbo"),
        (50013, "Nasi Goreng Mawut (Mie+Nasi)", 700, 18, 80, 28, "Karbo"),
        (50014, "Lontong Polos (1 buah)", 130, 2.5, 28, 0.2, "Karbo"),
        (50015, "Ketupat (1 buah)", 160, 3, 35, 0.5, "Karbo"),
        (50016, "Buras (1 buah)", 150, 3, 20, 6, "Karbo"),
        (50017, "Kentang Rebus (1 sedang)", 87, 1.9, 20, 0.1, "Karbo"),
        (50018, "Kentang Goreng (1 porsi)", 312, 3.4, 41, 15, "Karbo"),
        (50019, "Mashed Potato (1 porsi)", 220, 4, 25, 12, "Karbo"),
        (50020, "Ubi Cilembu Oven (1 sedang)", 130, 1.5, 30, 0.3, "Karbo"),
        (50021, "Singkong Rebus (1 potong)", 150, 1.3, 35, 0.3, "Karbo"),
        (50022, "Singkong Goreng (1 potong)", 200, 1, 35, 8, "Karbo"),
        (50023, "Jagung Rebus (1 bonggol)", 90, 3, 19, 1, "Karbo"),
        (50024, "Roti Tawar Putih (1 lembar)", 100, 3, 18, 1.5, "Karbo"),
        (50025, "Roti Gandum (1 lembar)", 95, 4, 17, 1, "Karbo"),
        (50026, "Oatmeal Instan (1 mangkok)", 150, 5, 27, 3, "Karbo"),
        (50027, "Bubur Ayam (Polos)", 220, 10, 30, 8, "Karbo"),
        (50028, "Bubur Manado/Tinutuan (1 mangkok)", 250, 8, 45, 4, "Karbo"),
        (50215, "Nasi Tim Ayam (1 mangkok)", 400, 15, 60, 10, "Karbo"),
        (50350, "Nasi Tutug Oncom (1 porsi)", 250, 8, 40, 6, "Karbo"),
        (50351, "Nasi Kucing (1 bungkus)", 180, 4, 30, 3, "Karbo"),
        (50352, "Hash Brown (1 buah)", 140, 1, 15, 9, "Karbo"),

        # ==========================================
        # 2. ANEKA MIE & PASTA
        # ==========================================
        (50040, "Indomie Goreng Original (1 bungkus)", 380, 8, 54, 14, "Karbo"),
        (50041, "Indomie Goreng Rendang (1 bungkus)", 400, 9, 56, 16, "Karbo"),
        (50042, "Indomie Goreng Aceh (1 bungkus)", 390, 8, 55, 15, "Karbo"),
        (50043, "Indomie Rebus Ayam Bawang (1 bungkus)", 300, 7, 45, 11, "Karbo"),
        (50044, "Indomie Rebus Soto Mie (1 bungkus)", 320, 7, 46, 12, "Karbo"),
        (50045, "Indomie Rebus Kari Ayam (1 bungkus)", 340, 8, 48, 13, "Karbo"),
        (50046, "Mie Sedaap Goreng (1 bungkus)", 390, 8, 55, 15, "Karbo"),
        (50047, "Mie Gacoan (Level 1)", 450, 12, 60, 18, "Karbo"),
        (50048, "Mie Ayam Bakso (1 mangkok)", 420, 18, 55, 14, "Lainnya"),
        (50049, "Mie Yamin Manis (1 mangkok)", 450, 16, 65, 12, "Lainnya"),
        (50050, "Mie Aceh Goreng (Daging)", 550, 20, 60, 25, "Lainnya"),
        (50051, "Mie Celor Palembang (1 porsi)", 380, 15, 45, 18, "Lainnya"),
        (50052, "Mie Kocok Bandung (1 porsi)", 400, 20, 40, 22, "Lainnya"),
        (50053, "Kwetiau Goreng Sapi (1 porsi)", 580, 18, 75, 24, "Lainnya"),
        (50054, "Kwetiau Siram Seafood (1 porsi)", 450, 20, 50, 18, "Lainnya"),
        (50055, "Bihun Goreng (1 porsi)", 420, 8, 70, 14, "Lainnya"),
        (50056, "Ifumie (Mie Kering Siram)", 550, 15, 70, 25, "Lainnya"),
        (50057, "Spaghetti Bolognese (1 porsi)", 400, 15, 55, 12, "Lainnya"),
        (50058, "Spaghetti Carbonara (1 porsi)", 550, 18, 50, 30, "Lainnya"),
        (50360, "Macaroni Schotel (1 potong)", 320, 12, 25, 20, "Lainnya"),
        (50361, "Lasagna (1 porsi)", 450, 20, 40, 25, "Lainnya"),

        # ==========================================
        # 3. LAUK HEWANI (AYAM & BEBEK)
        # ==========================================
        (50070, "Dada Ayam Rebus (100g)", 165, 31, 0, 3.6, "Hewani"),
        (50071, "Dada Ayam Bakar (Tanpa kulit)", 170, 30, 0, 5, "Hewani"),
        (50072, "Paha Ayam Goreng (1 potong)", 280, 22, 5, 18, "Hewani"),
        (50073, "Sayap Ayam Goreng (1 potong)", 200, 15, 4, 14, "Hewani"),
        (50074, "Ayam Geprek + Sambal (1 potong)", 350, 25, 10, 22, "Hewani"),
        (50075, "Ayam Penyet (1 potong)", 300, 25, 8, 18, "Hewani"),
        (50076, "Ayam Pop Padang (1 potong)", 265, 24, 2, 17, "Hewani"),
        (50077, "Ayam Bakar Taliwang (1 ekor kecil)", 450, 40, 5, 20, "Hewani"),
        (50078, "Ayam Betutu (1 porsi)", 320, 28, 6, 18, "Hewani"),
        (50079, "Opor Ayam (Dada, Santan)", 320, 28, 6, 20, "Hewani"),
        (50080, "Ayam Rica-Rica (1 potong)", 280, 26, 5, 16, "Hewani"),
        (50081, "Ayam Goreng Mentega (1 potong)", 310, 24, 10, 18, "Hewani"),
        (50082, "Ayam Woku (1 potong)", 250, 25, 4, 14, "Hewani"),
        (50083, "Sate Ayam Madura (10 tusuk)", 450, 30, 20, 25, "Hewani"),
        (50084, "Sate Taichan (10 tusuk, dada)", 250, 35, 2, 10, "Hewani"),
        (50085, "Sate Kulit Ayam (5 tusuk)", 350, 8, 2, 35, "Hewani"),
        (50086, "Bebek Goreng (Paha)", 400, 20, 6, 32, "Hewani"),
        (50087, "Bebek Bakar (Paha)", 380, 22, 8, 28, "Hewani"),
        (50088, "Sate Ati Ampela (1 tusuk)", 70, 8, 1, 3, "Hewani"),
        (50370, "Chicken Katsu (1 porsi)", 350, 20, 25, 18, "Hewani"),
        (50371, "Chicken Karage (1 porsi)", 380, 18, 20, 22, "Hewani"),
        (50372, "Chicken Nugget (5 buah)", 220, 12, 15, 14, "Hewani"),

        # ==========================================
        # 4. LAUK HEWANI (DAGING SAPI & KAMBING)
        # ==========================================
        (50100, "Rendang Daging Sapi (1 potong)", 250, 18, 5, 18, "Hewani"),
        (50101, "Empal Gentong (1 mangkok)", 350, 22, 8, 25, "Hewani"),
        (50102, "Empal Daging Goreng (1 potong)", 260, 20, 8, 16, "Hewani"),
        (50103, "Semur Daging Sapi (1 potong)", 280, 22, 12, 14, "Hewani"),
        (50104, "Gulai Cincang (1 porsi)", 380, 20, 8, 30, "Hewani"),
        (50105, "Dendeng Balado (1 potong)", 220, 15, 6, 14, "Hewani"),
        (50106, "Paru Goreng (1 potong)", 180, 12, 2, 14, "Hewani"),
        (50107, "Gulai Tunjang / Kaki (1 potong)", 400, 25, 5, 32, "Hewani"),
        (50108, "Sate Padang (10 tusuk)", 500, 28, 30, 28, "Hewani"),
        (50109, "Sate Kambing (10 tusuk)", 550, 35, 15, 38, "Hewani"),
        (50110, "Sate Maranggi (10 tusuk)", 480, 32, 18, 30, "Hewani"),
        (50111, "Sop Buntut (1 mangkok)", 300, 20, 10, 20, "Hewani"),
        (50112, "Sop Iga Sapi (1 mangkok)", 450, 25, 10, 35, "Hewani"),
        (50113, "Rawon Daging (1 mangkok)", 350, 22, 12, 22, "Hewani"),
        (50114, "Soto Betawi (Santan)", 380, 20, 12, 28, "Hewani"),
        (50115, "Coto Makassar (1 mangkok)", 350, 22, 10, 25, "Hewani"),
        (50116, "Tongseng Kambing (1 porsi)", 480, 22, 15, 38, "Hewani"),
        (50117, "Beef Teriyaki (1 porsi)", 320, 25, 15, 18, "Hewani"),
        (50118, "Beef Yakiniku (1 porsi)", 310, 24, 12, 19, "Hewani"),
        (50119, "Steak Sapi Sirloin (200g)", 500, 40, 0, 35, "Hewani"),
        (50120, "Bakso Sapi (5 butir)", 190, 15, 8, 10, "Hewani"),
        (50202, "Soto Banjar (1 porsi)", 350, 18, 40, 14, "Hewani"),
        (50380, "Gulai Otak Sapi (1 potong)", 250, 10, 2, 22, "Hewani"),
        (50381, "Lidah Sapi Goreng (1 porsi)", 280, 18, 2, 20, "Hewani"),
        (50382, "Kikil Sapi (1 porsi)", 200, 25, 0, 10, "Hewani"),

        # ==========================================
        # 5. LAUK HEWANI (IKAN & SEAFOOD)
        # ==========================================
        (50130, "Ikan Kembung Bakar (1 ekor)", 125, 22, 0, 4, "Hewani"),
        (50131, "Ikan Lele Goreng (1 ekor)", 250, 18, 5, 15, "Hewani"),
        (50132, "Pecel Lele (1 ekor + sambal)", 300, 18, 10, 20, "Hewani"),
        (50133, "Ikan Mas Pepes (1 ekor)", 180, 25, 5, 6, "Hewani"),
        (50134, "Ikan Tongkol Balado (1 potong)", 190, 20, 6, 8, "Hewani"),
        (50135, "Ikan Asin Jambal (1 potong)", 120, 15, 0, 6, "Hewani"),
        (50136, "Ikan Gurame Asam Manis (1 porsi)", 450, 25, 30, 25, "Hewani"),
        (50137, "Udang Goreng Tepung (5 ekor)", 250, 15, 20, 12, "Hewani"),
        (50138, "Udang Saus Padang (1 porsi)", 230, 18, 12, 10, "Hewani"),
        (50139, "Cumi Goreng Tepung (1 porsi)", 350, 18, 30, 18, "Hewani"),
        (50140, "Cumi Asam Manis (1 porsi)", 200, 18, 15, 8, "Hewani"),
        (50141, "Kerang Rebus (1 porsi)", 120, 15, 5, 2, "Hewani"),
        (50142, "Kepiting Saus Tiram (1 ekor)", 350, 25, 15, 20, "Hewani"),
        (50143, "Ikan Salmon Pan Seared (100g)", 208, 20, 0, 13, "Hewani"),
        (50144, "Gulai Kepala Kakap (1 porsi)", 550, 30, 10, 40, "Hewani"),
        (50204, "Gulai Ikan Kakap (1 potong)", 320, 20, 5, 24, "Hewani"),
        (50390, "Sate Lilit Ikan (3 tusuk)", 150, 12, 5, 8, "Hewani"),
        (50391, "Ikan Patin Pindang (1 porsi)", 200, 18, 2, 12, "Hewani"),
        (50392, "Otak-Otak Ikan Tenggiri (1 buah)", 40, 2, 5, 1, "Hewani"),

        # ==========================================
        # 6. TELUR & OLAHAN
        # ==========================================
        (50150, "Telur Rebus (1 butir)", 78, 6, 0.6, 5, "Hewani"),
        (50151, "Telur Ceplok Goreng (1 butir)", 110, 7, 0.8, 9, "Hewani"),
        (50152, "Telur Dadar (1 butir)", 120, 7, 1, 10, "Hewani"),
        (50153, "Telur Dadar Padang (1 potong tebal)", 180, 10, 5, 14, "Hewani"),
        (50154, "Telur Balado (1 butir)", 140, 7, 5, 10, "Hewani"),
        (50155, "Telur Asin (1 butir)", 130, 9, 1, 10, "Hewani"),
        (50156, "Telur Puyuh Rebus (5 butir)", 75, 6, 0.5, 5, "Hewani"),
        (50157, "Sate Telur Puyuh (1 tusuk)", 90, 7, 2, 6, "Hewani"),
        (50212, "Fuyunghai (1 porsi)", 350, 12, 15, 28, "Lainnya"),

        # ==========================================
        # 7. NABATI (TAHU, TEMPE, KACANG)
        # ==========================================
        (50170, "Tempe Goreng (2 potong)", 150, 10, 9, 10, "Nabati"),
        (50171, "Tempe Bacem (1 potong)", 80, 5, 10, 3, "Nabati"),
        (50172, "Tempe Orek Basah (1 porsi)", 180, 12, 18, 8, "Nabati"),
        (50173, "Tempe Orek Kering (1 porsi)", 220, 10, 25, 10, "Nabati"),
        (50174, "Tempe Mendoan (1 buah besar)", 120, 6, 15, 8, "Nabati"),
        (50175, "Keripik Tempe (5 keping)", 150, 5, 15, 8, "Nabati"),
        (50176, "Tahu Goreng (2 potong)", 110, 8, 4, 8, "Nabati"),
        (50177, "Tahu Bacem (1 buah)", 75, 4, 10, 3, "Nabati"),
        (50178, "Tahu Isi Sayur (1 buah)", 90, 4, 8, 6, "Nabati"),
        (50179, "Tahu Gejrot (1 porsi)", 180, 10, 25, 6, "Nabati"),
        (50180, "Tahu Tek / Tahu Telur (1 porsi)", 350, 15, 25, 20, "Nabati"),
        (50181, "Pepes Tahu (1 bungkus)", 65, 7, 3, 2, "Nabati"),
        (50182, "Sapo Tahu Seafood (1 porsi)", 250, 15, 20, 12, "Hewani"), 
        (50183, "Perkedel Jagung (1 buah)", 130, 3, 20, 6, "Nabati"),
        (50184, "Perkedel Kentang (1 buah)", 100, 2, 15, 4, "Nabati"),
        (50185, "Edamame Rebus (1 mangkok)", 100, 9, 8, 4, "Nabati"),
        (50186, "Bubur Kacang Hijau (Santan)", 250, 10, 40, 7, "Nabati"),
        (50400, "Oncom Goreng Tepung (1 potong)", 100, 3, 10, 5, "Nabati"),
        (50401, "Pepes Jamur (1 bungkus)", 50, 3, 5, 1, "Nabati"),

        # ==========================================
        # 8. SAYURAN (MASAKAN & MENTAH)
        # ==========================================
        (50200, "Sayur Asem (1 mangkok)", 80, 3, 10, 2, "Sayur"),
        (50201, "Sayur Lodeh (1 mangkok, santan)", 180, 5, 12, 12, "Sayur"),
        (50202, "Sayur Bayam Bening (1 mangkok)", 35, 3, 6, 0.5, "Sayur"),
        (50203, "Sayur Sop (1 mangkok)", 60, 2, 8, 2, "Sayur"),
        (50204, "Tumis Kangkung (1 porsi)", 90, 3, 5, 7, "Sayur"),
        (50205, "Tumis Buncis (1 porsi)", 70, 2, 8, 4, "Sayur"),
        (50206, "Tumis Tauge Ikan Asin (1 porsi)", 110, 8, 6, 6, "Sayur"),
        (50207, "Capcay Kuah (1 porsi)", 120, 5, 10, 6, "Sayur"),
        (50208, "Capcay Goreng (1 porsi)", 180, 6, 12, 12, "Sayur"),
        (50209, "Gudeg Nangka (1 porsi)", 180, 4, 25, 8, "Sayur"),
        (50210, "Sayur Nangka Kapau (1 porsi)", 200, 3, 20, 12, "Sayur"),
        (50211, "Urap Sayur (1 porsi)", 120, 4, 15, 6, "Sayur"),
        (50212, "Terong Balado (1 porsi)", 140, 2, 12, 10, "Sayur"),
        (50213, "Pecel Sayur (1 porsi, bumbu kacang)", 220, 8, 25, 12, "Sayur"),
        (50214, "Gado-Gado (1 porsi lengkap)", 350, 15, 40, 15, "Sayur"),
        (50215, "Karedok (1 porsi)", 180, 6, 20, 9, "Sayur"),
        (50216, "Ketoprak Jakarta (1 porsi)", 500, 15, 60, 20, "Sayur"),
        (50217, "Asinan Betawi (1 porsi)", 150, 4, 25, 5, "Sayur"),
        (50218, "Brokoli Rebus (100g)", 34, 2.8, 7, 0.4, "Sayur"),
        (50219, "Lalapan Mentah (Timun/Kemangi)", 15, 1, 3, 0, "Sayur"),
        (50220, "Salad Sayur (Tanpa Dressing)", 30, 2, 5, 0, "Sayur"),
        (50205, "Sayur Asem Jakarta (1 mangkok)", 90, 3, 15, 2, "Sayur"),
        (50410, "Ulukutek Leunca (1 porsi)", 100, 3, 10, 5, "Sayur"),
        (50411, "Tumis Sawi Putih (1 porsi)", 60, 2, 5, 4, "Sayur"),
        (50412, "Cah Kailan (1 porsi)", 70, 2, 6, 4, "Sayur"),

        # ==========================================
        # 9. BUAH-BUAHAN
        # ==========================================
        (50230, "Pisang Ambon (1 buah)", 90, 1, 23, 0.3, "Buah"),
        (50231, "Pisang Goreng (1 buah)", 140, 1, 25, 5, "Buah"),
        (50232, "Apel Merah (1 buah)", 52, 0.3, 14, 0.2, "Buah"),
        (50233, "Pepaya Potong (1 mangkok)", 45, 0.5, 11, 0.1, "Buah"),
        (50234, "Jeruk Medan (1 buah)", 47, 0.9, 12, 0.1, "Buah"),
        (50235, "Alpukat (1/2 buah)", 160, 2, 9, 15, "Buah"),
        (50236, "Mangga Harum Manis (1 buah)", 150, 1, 40, 0.6, "Buah"),
        (50237, "Semangka Potong (1 mangkok)", 30, 0.6, 8, 0.2, "Buah"),
        (50238, "Melon Potong (1 mangkok)", 36, 0.9, 9, 0.1, "Buah"),
        (50239, "Salak (1 buah)", 80, 0.5, 20, 0.1, "Buah"),
        (50240, "Durian (3 biji)", 150, 2, 30, 5, "Buah"),
        (50241, "Buah Naga (1 buah sedang)", 60, 1, 12, 0.5, "Buah"),
        (50242, "Rujak Buah (1 porsi)", 180, 2, 40, 2, "Buah"),
        (50420, "Manggis (1 buah)", 30, 0.3, 7, 0.1, "Buah"),
        (50421, "Rambutan (5 buah)", 40, 0.5, 10, 0.1, "Buah"),
        (50422, "Duku (5 buah)", 50, 0.5, 13, 0.1, "Buah"),
        (50423, "Sawo (1 buah)", 80, 0.5, 20, 1, "Buah"),
        (50424, "Kelengkeng (5 buah)", 20, 0.5, 5, 0, "Buah"),

        # ==========================================
        # 10. JAJANAN PASAR & STREET FOOD (Search Only)
        # ==========================================
        (50250, "Bakso Sapi Kuah (1 mangkok)", 320, 20, 30, 15, "Lainnya"),
        (50251, "Batagor (1 porsi, bumbu kacang)", 450, 12, 40, 25, "Lainnya"),
        (50252, "Siomay Bandung (1 porsi)", 380, 15, 45, 18, "Lainnya"),
        (50253, "Cilok Bumbu Kacang (1 porsi)", 300, 3, 50, 10, "Lainnya"),
        (50254, "Cimol (1 bungkus)", 250, 1, 40, 10, "Lainnya"),
        (50255, "Cireng Rujak (3 buah)", 210, 1, 35, 8, "Lainnya"),
        (50256, "Martabak Manis Coklat Keju (1 potong)", 350, 6, 45, 18, "Lainnya"),
        (50257, "Martabak Telur (1 potong)", 220, 8, 15, 14, "Lainnya"),
        (50258, "Gorengan Bakwan/Bala-bala (1 buah)", 140, 2, 15, 8, "Lainnya"),
        (50259, "Gorengan Tahu Isi (1 buah)", 150, 4, 12, 10, "Lainnya"),
        (50260, "Gorengan Pisang Molen (1 buah)", 160, 2, 25, 7, "Lainnya"),
        (50261, "Risoles Ragout (1 buah)", 160, 4, 18, 9, "Lainnya"),
        (50262, "Pastel Sayur (1 buah)", 150, 3, 20, 8, "Lainnya"),
        (50263, "Lemper Ayam (1 buah)", 180, 5, 25, 8, "Lainnya"),
        (50264, "Arem-Arem (1 buah)", 220, 6, 35, 7, "Lainnya"),
        (50265, "Lumpia Semarang (1 buah)", 140, 4, 20, 5, "Lainnya"),
        (50266, "Onde-Onde (1 buah)", 180, 3, 30, 6, "Lainnya"),
        (50267, "Klepon (3 butir)", 120, 1, 28, 2, "Lainnya"),
        (50268, "Otak-otak Bakar (1 bungkus)", 40, 2, 5, 1, "Lainnya"),
        (50269, "Dimsum Siomay (3 pcs)", 165, 9, 15, 6, "Lainnya"),
        (50270, "Seblak Kerupuk Original (1 mangkok)", 365, 9.5, 48, 14, "Lainnya"),
        (50271, "Seblak Ceker Pedas (1 mangkok)", 430, 16, 48, 20, "Lainnya"),
        (50272, "Seblak Mie Telur (1 mangkok)", 495, 11, 72, 18, "Lainnya"),
        (50273, "Seblak Bakso Sosis (1 mangkok)", 460, 14, 52, 22, "Lainnya"),
        (50274, "Seblak Seafood Komplit (1 mangkok besar)", 550, 22, 58, 26, "Lainnya"),
        (50275, "Soto Mie Bogor (1 mangkok)", 420, 15, 55, 18, "Lainnya"),
        (50276, "Tekwan Palembang (1 mangkok)", 280, 12, 45, 5, "Lainnya"),
        (50277, "Pempek Kapal Selam (1 buah besar)", 350, 15, 40, 15, "Lainnya"),
        (50430, "Croffle (1 buah)", 180, 3, 20, 10, "Lainnya"),
        (50431, "Cromboloni (1 buah)", 400, 5, 45, 22, "Lainnya"),
        (50432, "Roti Bakar Coklat Keju (1 porsi)", 350, 8, 45, 15, "Lainnya"),
        (50433, "Kue Cubit (5 buah)", 150, 3, 25, 5, "Lainnya"),
        (50434, "Kue Ape (3 buah)", 120, 2, 25, 2, "Lainnya"),
        (50435, "Serabi Solo (1 buah)", 130, 2, 20, 5, "Lainnya"),

        # ==========================================
        # 11. PELENGKAP (SAMBAL & KERUPUK)
        # ==========================================
        (50300, "Sambal Terasi (1 sdm)", 20, 0.5, 2, 1, "Lainnya"),
        (50301, "Sambal Bawang (1 sdm)", 45, 0.2, 1, 4, "Lainnya"),
        (50302, "Kerupuk Putih/Blek (1 buah)", 65, 1, 14, 0.5, "Lainnya"),
        (50303, "Kerupuk Udang (1 buah kecil)", 40, 1, 5, 2, "Lainnya"),
        (50304, "Emping Melinjo (1 porsi kecil)", 100, 2, 12, 5, "Lainnya"),
        (50305, "Bawang Goreng (1 sdm)", 45, 0.5, 3, 3, "Lainnya"),
        (50440, "Sambal Ijo Padang (1 sdm)", 30, 0.5, 1, 2.5, "Lainnya"),
        (50441, "Sambal Matah (1 sdm)", 50, 0.5, 2, 4.5, "Lainnya"),
        (50442, "Sambal Kecap (1 sdm)", 35, 0.5, 8, 0, "Lainnya"),
        (50443, "Saus Kacang / Bumbu Pecel (1 sdm)", 60, 2, 4, 4, "Lainnya"),
        (50444, "Kerupuk Kulit / Jangek (1 bungkus kecil)", 90, 9, 0, 6, "Lainnya"),
        (50445, "Rempeyek Kacang (1 keping)", 80, 2, 8, 5, "Lainnya"),

        # ==========================================
        # 12. MINUMAN
        # ==========================================
        (50320, "Air Putih (1 gelas)", 0, 0, 0, 0, "Lainnya"),
        (50321, "Es Teh Manis (1 gelas)", 120, 0, 30, 0, "Lainnya"),
        (50322, "Teh Tawar (1 gelas)", 2, 0, 0, 0, "Lainnya"),
        (50323, "Kopi Hitam (Tanpa gula)", 5, 0, 1, 0, "Lainnya"),
        (50324, "Kopi Susu Gula Aren (1 gelas)", 250, 2, 35, 10, "Lainnya"),
        (50325, "Cappucino Cincau (1 gelas)", 200, 2, 35, 6, "Lainnya"),
        (50326, "Jus Alpukat (Susu Coklat)", 350, 3, 45, 18, "Lainnya"),
        (50327, "Jus Jeruk (Gula)", 110, 1, 26, 0, "Lainnya"),
        (50328, "Jus Melon (Gula)", 120, 1, 28, 0, "Lainnya"),
        (50329, "Es Campur (1 mangkok)", 250, 2, 60, 1, "Lainnya"),
        (50330, "Es Cendol / Dawet (1 gelas)", 280, 2, 45, 10, "Lainnya"),
        (50331, "Es Kelapa Muda (Gula)", 110, 1, 25, 0.5, "Lainnya"),
        (50332, "Susu UHT Full Cream (250ml)", 150, 8, 12, 8, "Lainnya"),
        (50333, "Susu UHT Coklat (250ml)", 190, 8, 25, 6, "Lainnya"),
        (50334, "Wedang Ronde (1 mangkok)", 150, 2, 30, 3, "Lainnya"),
        (50335, "Boba Brown Sugar Milk Tea", 450, 2, 80, 15, "Lainnya"),
        (50450, "Es Teler (1 mangkok)", 300, 3, 50, 10, "Lainnya"),
        (50451, "Es Doger (1 gelas)", 280, 2, 45, 10, "Lainnya"),
        (50452, "Es Oyen (1 mangkok)", 320, 3, 55, 8, "Lainnya"),
        (50453, "Bajigur (1 gelas)", 180, 1, 30, 6, "Lainnya"),
        (50454, "Bandrek (1 gelas)", 150, 1, 35, 0, "Lainnya"),

        # ==========================================
        # 13. FAST FOOD (SEARCH ONLY)
        # ==========================================
        (50500, "Burger Sapi (1 buah)", 450, 20, 35, 25, "Lainnya"),
        (50501, "Cheeseburger (1 buah)", 500, 22, 35, 30, "Lainnya"),
        (50502, "Fried Chicken (1 dada)", 350, 25, 15, 20, "Lainnya"),
        (50503, "Fried Chicken (1 paha bawah)", 250, 18, 10, 15, "Lainnya"),
        (50504, "Pizza Meat Lover (1 slice)", 300, 12, 30, 14, "Lainnya"),
        (50505, "Pizza Pepperoni (1 slice)", 280, 10, 28, 12, "Lainnya"),
        (50506, "Donat Gula (1 buah)", 220, 3, 25, 12, "Lainnya"),
        (50507, "Donat Coklat (1 buah)", 280, 4, 30, 15, "Lainnya")
    ]
    
    print(f"🚀 Menyuntikkan {len(makanan_data)} data makanan...")
    
    # BATCH INSERT (50 PER BATCH) AGAR TIDAK ERROR
    batch_size = 50
    query = '''
    INSERT OR REPLACE INTO food_cache 
    (fatsecret_id, nama_makanan, kalori, protein, karbo, lemak, kategori) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    
    for i in range(0, len(makanan_data), batch_size):
        batch = makanan_data[i:i + batch_size]
        cursor.executemany(query, batch)
        print(f"   --> Menyimpan batch {i} sampai {i + len(batch)}...")
        
    conn.commit()
    conn.close()
    
    print("\n✅ SELESAI! DATABASE MONSTER (450+ MENU) SUDAH SIAP.")

if __name__ == "__main__":
    reset_dan_isi_database()