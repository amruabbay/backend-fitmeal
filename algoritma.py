import sqlite3
import random
import copy

DB_NAME = "skripsi_diet.db"

# ===========================================================
# ⛔ DAFTAR BLACKLIST (SUPER KETAT & LENGKAP)
# ===========================================================
# Makanan dengan kata-kata ini TIDAK AKAN MUNCUL di Rencana Diet,
# tapi tetap bisa dicari manual di tab Search.
BLACKLIST_KEYWORDS = [
    # 1. Fast Food & Junk Food (Merk & Jenis)
    "kfc", "mcd", "mcdonalds", "burger", "pizza", "hokben", "solaria",
    "a&w", "wendys", "fast food", "junk food", "french fries", "kentang goreng",
    "hotdog", "corndog", "chicken wings", "chicken nugget", "nugget",
    "kebab", "shawarma", "doner", "taco", "burrito",
    "sushi", "ramen", "tempura", "dimsum", "takoyaki",
    "croffle", "cromboloni", "toast", "dessert box",  # Jajanan Viral
    
    # 2. Olahan Minyak & Gorengan Berat
    "gorengan", "crispy", "penyet", "geprek", "kulit ayam", "kulit",
    "fried chicken", "ayam goreng", "bebek goreng", "lele goreng", 
    "bakwan", "bala-bala", "cireng", "cimol", "cilok", "batagor", "pempek",
    "kerupuk", "krupuk", "rempeyek", "emping", "mendoan", "risol", "lumpia", 
    "pastel", "basreng", "kripik", "keripik", "chiki", "seblak", "cuanki", "maklor", "cilor",
    "tahu tek", "tahu campur", "tahu gejrot", "lontong balap",
    
    # 3. Lemak Tinggi, Santan & Jeroan
    "santan", "gulai", "rendang", "tongseng", "opor", "soto betawi", "sayur lodeh",
    "jeroan", "usus", "babat", "kikil", "tunjang", "otak", "paru", "ati ampela",
    "sate kambing", "sate padang", "sate kulit", "rawon", 
    "gajih", "lemak", "minyak",
    
    # 4. Karbo Olahan & Instan (High GI)
    "indomie", "mie instan", "mie goreng", "mie rebus", "sosis", "kornet", "kaleng",
    "kwetiau", "bihun goreng", "ifumie", "nasgor", "nasi goreng", 
    "nasi uduk", "nasi kuning", "nasi liwet", "nasi hainam", "nasi kebuli", "lontong sayur", "ketoprak",
    "martabak", "roti bakar", "kue", "gacoan", "bakso", "baso", "mie ayam", "pangsit", "bakmi",
    "biskuit", "wafer", "cake", "pudding", "crepes", "pukis", "pancong", "kue cubit",
    
    # 5. Minuman Manis & Dessert
    "boba", "bubble", "milk tea", "chatime", "starbucks",
    "kopi susu", "cappucino", "latte", "frappe", "smoothie", "kopi", "teh",
    "es teh manis", "teh tarik", "es campur", "es teler", "es doger", "es krim", "ice cream",
    "coklat", "chocolate", "brown sugar", "gula aren", "sirup", "soda",
    "susu kental manis", "skm", "full cream"
]

# ===========================================================
# 🧮 HITUNG TARGET MACRO (Kalori → Protein, Karbo, Lemak)
# ===========================================================
def hitung_macro_targets(target_kalori, target_protein):
    """
    Mengubah target_kalori & target_protein menjadi target lengkap 4 macro.
    Sisa kalori setelah protein dibagi: 60% Karbo, 40% Lemak.
    """
    protein_kal = target_protein * 4  # 1g protein = 4 kcal
    remaining_kal = max(target_kalori - protein_kal, 0)
    
    carb_kal = remaining_kal * 0.60   # 60% sisa dari karbo
    fat_kal  = remaining_kal * 0.40   # 40% sisa dari lemak

    return {
        'kalori':  target_kalori,
        'protein': target_protein,
        'karbo':   round(carb_kal / 4, 1),  # 1g karbo = 4 kcal
        'lemak':   round(fat_kal / 9, 1),   # 1g lemak = 9 kcal
    }


# ===========================================================
# 📊 HITUNG FITNESS SCORE (Multi-Objective)
# ===========================================================
def hitung_fitness_score(pagi, siang, malam, targets):
    """
    Menghitung seberapa "bagus" sebuah menu harian.
    Skor RENDAH = BAGUS. Skor 0 = SEMPURNA.
    
    Bobot:
    - Kalori : 1.0 (basis)
    - Protein: 4.0 (paling penting untuk diet/bulking)
    - Lemak  : 2.0 (penting untuk kenyang & hormon)
    - Karbo  : 1.0 (fleksibel)
    
    Bonus: Distribusi kalori per meal yang seimbang.
    """
    all_items = pagi + siang + malam
    
    total_kal  = sum(i['kalori']  for i in all_items)
    total_pro  = sum(i['protein'] for i in all_items)
    total_fat  = sum(i['lemak']   for i in all_items)
    total_carb = sum(i['karbo']   for i in all_items)
    
    # --- SKOR UTAMA: Jarak ke target ---
    score = (
        abs(targets['kalori']  - total_kal)  * 1.0 +
        abs(targets['protein'] - total_pro)  * 4.0 +
        abs(targets['lemak']   - total_fat)  * 2.0 +
        abs(targets['karbo']   - total_carb) * 1.0
    )
    
    # --- PENALTI DISTRIBUSI MEAL ---
    # Idealnya: Pagi 25-30%, Siang 35-40%, Malam 30-35%
    # Kita penalize jika satu meal terlalu besar atau terlalu kecil.
    target_kal = targets['kalori']
    if target_kal > 0:
        kal_pagi  = sum(i['kalori'] for i in pagi)
        kal_siang = sum(i['kalori'] for i in siang)
        kal_malam = sum(i['kalori'] for i in malam)
        
        # Rasio ideal per meal
        rasio_pagi  = kal_pagi  / target_kal if target_kal else 0
        rasio_siang = kal_siang / target_kal if target_kal else 0
        rasio_malam = kal_malam / target_kal if target_kal else 0
        
        # Penalti jika jauh dari rasio ideal (soft constraint)
        penalty = 0
        penalty += max(0, abs(rasio_pagi  - 0.275) - 0.05) * target_kal * 0.5
        penalty += max(0, abs(rasio_siang - 0.375) - 0.05) * target_kal * 0.5
        penalty += max(0, abs(rasio_malam - 0.325) - 0.05) * target_kal * 0.5
        
        score += penalty
    
    return score


# ===========================================================
# 📦 AMBIL DATA LOKAL (FILTERED) — Tidak berubah
# ===========================================================
def ambil_data_lokal():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM food_cache")
    raw_data = cursor.fetchall()
    conn.close()
    
    dataset = {
        'Karbo': [],
        'Hewani': [],
        'Nabati': [],
        'Sayur': [],
        'Buah': [],
        'Lainnya': []
    }
    
    for row in raw_data:
        try:
            nama_makanan = row['nama_makanan']
            nama_lower = nama_makanan.lower()
            
            # --- FILTER 1: BLACKLIST KEYWORDS ---
            if any(bad_word in nama_lower for bad_word in BLACKLIST_KEYWORDS):
                continue 
            
            # --- FILTER 2: KATEGORI LAINNYA ---
            if row['kategori'] == 'Lainnya':
                continue

            clean_id = int(row['fatsecret_id'])
            
            item = {
                'id': clean_id, 
                'nama_makanan': nama_makanan,
                'kalori': float(row['kalori']),
                'protein': float(row['protein']),
                'karbo': float(row['karbo']),
                'lemak': float(row['lemak'])
            }
            
            kategori = row['kategori']
            if kategori in dataset:
                dataset[kategori].append(item)
                
        except ValueError:
            continue
            
    return dataset


# ===========================================================
# 🔍 CARI KATEGORI — Helper untuk mutasi
# ===========================================================
def cari_kategori(item, dataset):
    """Cari kategori sebuah item berdasarkan ID-nya."""
    for kategori, items in dataset.items():
        for food in items:
            if food['id'] == item['id']:
                return kategori
    return None


# ===========================================================
# 🍽️ SUSUN PIRING (4 Sehat) — Logika "Isi Piringku" Kemenkes
# ===========================================================
def susun_piring(dataset):
    piring = []
    
    # 1. Makanan Pokok (Karbo) — Wajib
    if dataset['Karbo']: 
        piring.append(random.choice(dataset['Karbo']))
    
    # 2. Lauk Pauk — Variasi Hewani + Nabati
    if dataset['Hewani'] and random.random() > 0.1:  # 90% ada hewani
        piring.append(random.choice(dataset['Hewani']))
        
    if dataset['Nabati'] and random.random() > 0.3:  # 70% ada nabati
        piring.append(random.choice(dataset['Nabati']))
    
    # 3. Sayuran — Wajib
    if dataset['Sayur']: 
        piring.append(random.choice(dataset['Sayur']))
    
    # 4. Buah — Opsional 50%
    if dataset['Buah'] and random.random() > 0.5:
        piring.append(random.choice(dataset['Buah']))
        
    return piring


# ===========================================================
# 🧬 MUTASI PIRING — Swap 1 item dengan item dari kategori sama
# ===========================================================
def mutasi_piring(piring, dataset):
    """
    Mengambil 1 item acak dari piring, lalu menggantinya
    dengan item lain dari KATEGORI YANG SAMA.
    Ini menjaga struktur "Isi Piringku" tetap utuh.
    """
    if not piring:
        return piring
    
    new_piring = copy.copy(piring)
    idx = random.randint(0, len(new_piring) - 1)
    old_item = new_piring[idx]
    
    # Cari kategori item yang mau diganti
    kategori = cari_kategori(old_item, dataset)
    
    if kategori and dataset[kategori]:
        # Pilih item baru yang berbeda (jika memungkinkan)
        candidates = [f for f in dataset[kategori] if f['id'] != old_item['id']]
        if candidates:
            new_piring[idx] = random.choice(candidates)
    
    return new_piring


# ===========================================================
# 🏔️ HILL CLIMBING — Optimasi Lokal per Run
# ===========================================================
def hill_climb(dataset, targets, iterasi=1500):
    """
    Satu sesi Hill Climbing:
    1. Mulai dari menu acak.
    2. Mutasi salah satu meal (Pagi/Siang/Malam).
    3. Jika hasilnya LEBIH BAIK, simpan. Jika tidak, buang.
    4. Ulangi sebanyak `iterasi` kali.
    """
    # Generate starting point
    pagi  = susun_piring(dataset)
    siang = susun_piring(dataset)
    malam = susun_piring(dataset)
    
    best_score = hitung_fitness_score(pagi, siang, malam, targets)
    
    for _ in range(iterasi):
        # Pilih meal mana yang akan dimutasi (acak)
        meal_choice = random.randint(0, 2)
        
        if meal_choice == 0:
            new_pagi = mutasi_piring(pagi, dataset)
            new_score = hitung_fitness_score(new_pagi, siang, malam, targets)
            if new_score < best_score:
                pagi = new_pagi
                best_score = new_score
                
        elif meal_choice == 1:
            new_siang = mutasi_piring(siang, dataset)
            new_score = hitung_fitness_score(pagi, new_siang, malam, targets)
            if new_score < best_score:
                siang = new_siang
                best_score = new_score
                
        else:
            new_malam = mutasi_piring(malam, dataset)
            new_score = hitung_fitness_score(pagi, siang, new_malam, targets)
            if new_score < best_score:
                malam = new_malam
                best_score = new_score
    
    return pagi, siang, malam, best_score


# ===========================================================
# 🚀 ALGORITMA UTAMA — Hill Climbing dengan Multi-Restart
# ===========================================================
def jalankan_algoritma(target_kalori, target_protein):
    """
    Fungsi utama yang dipanggil oleh main.py.
    
    Strategi: Jalankan Hill Climbing dari 5 titik awal berbeda,
    lalu ambil hasil TERBAIK dari semua run.
    Ini menghindari "terjebak" di solusi lokal yang buruk.
    
    Signature & return format SAMA dengan versi lama
    agar main.py tidak perlu diubah.
    """
    dataset = ambil_data_lokal()
    
    # Validasi: Pastikan stok makanan cukup
    if not dataset['Karbo'] or not dataset['Hewani']:
        print("⚠️ Warning: Database kekurangan menu sehat.")
        return [], {}
    
    # Hitung target macro lengkap (Kalori + Protein + Karbo + Lemak)
    targets = hitung_macro_targets(target_kalori, target_protein)
    
    # --- MULTI-RESTART HILL CLIMBING ---
    NUM_RESTARTS = 5
    MUTATIONS_PER_RUN = 1500
    
    best_overall_score = 999999
    best_pagi  = []
    best_siang = []
    best_malam = []
    
    for _ in range(NUM_RESTARTS):
        pagi, siang, malam, score = hill_climb(
            dataset, targets, iterasi=MUTATIONS_PER_RUN
        )
        
        if score < best_overall_score:
            best_overall_score = score
            best_pagi  = pagi
            best_siang = siang
            best_malam = malam
    
    # --- HITUNG STATISTIK HASIL ---
    all_items = best_pagi + best_siang + best_malam
    
    achieved = {
        'kalori':  round(sum(i['kalori']  for i in all_items), 1),
        'protein': round(sum(i['protein'] for i in all_items), 1),
        'karbo':   round(sum(i['karbo']   for i in all_items), 1),
        'lemak':   round(sum(i['lemak']   for i in all_items), 1),
    }
    
    # Akurasi (%) — seberapa dekat dengan target
    accuracy = {}
    for macro in ['kalori', 'protein', 'karbo', 'lemak']:
        if targets[macro] > 0:
            pct = (1 - abs(targets[macro] - achieved[macro]) / targets[macro]) * 100
            accuracy[macro] = round(max(pct, 0), 1)
        else:
            accuracy[macro] = 100.0
    
    # --- FORMAT OUTPUT (backward-compatible) ---
    menu_terbaik = [
        {"waktu": "Pagi",   "isi": best_pagi},
        {"waktu": "Siang",  "isi": best_siang},
        {"waktu": "Malam",  "isi": best_malam}
    ]
    
    stats = {
        "best_diff": round(best_overall_score, 1),   # Backward compat
        "algorithm": "Hill Climbing (Multi-Restart)",
        "restarts": NUM_RESTARTS,
        "mutations_per_run": MUTATIONS_PER_RUN,
        "target_macros": targets,
        "achieved_macros": achieved,
        "accuracy_pct": accuracy,
    }
    
    return menu_terbaik, stats