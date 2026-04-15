"""
==========================================================
📦 IMPORT DATA CSV → food_cache (dengan Auto-Kategori)
==========================================================
Script ini membaca datafoods.csv dan memasukkannya ke tabel
food_cache agar bisa digunakan oleh algoritma rekomendasi.

Fitur:
- Auto-kategorikan makanan menjadi: Karbo, Hewani, Nabati, Sayur, Buah
- Skip makanan yang masuk kategori "Lainnya" (junk food, snack, dll)
- Hindari duplikat berdasarkan nama makanan
- Gunakan fatsecret_id mulai dari 60001 agar tidak bentrok
"""

import sqlite3
import csv

DB_NAME = "skripsi_diet.db"
CSV_FILE = "datafoods.csv"

# ===========================================================
# 🏷️ KEYWORD KATEGORI — Untuk auto-assign kategori
# ===========================================================

KATEGORI_BUAH = [
    "apel", "pisang", "mangga", "jeruk", "semangka", "melon", "pepaya",
    "nanas", "anggur", "salak", "duku", "rambutan", "durian", "jambu",
    "manggis", "sirsak", "nangka masak", "sawo", "kesemek", "belimbing",
    "arbei", "strawberry", "alpukat", "lemon", "markisa", "buah naga",
    "buah nona", "embacang", "kokosan", "langsat", "matoa", "menteng",
    "srikaya", "duwet", "kedondong", "gandaria", "biwah", "bit",
    "bengkuang", "buah rotan", "buah rukam", "buah tuppa", "buah mentega",
    "buah merah", "buah negri", "buah atung", "buah kom",
    "rambutan", "tomat", "wortel", # wortel & tomat bisa buah/sayur
]

KATEGORI_SAYUR = [
    "bayam", "kangkung", "sawi", "brokoli", "kubis", "kol",
    "buncis", "kacang panjang", "terong", "labu", "pare", "paria",
    "oyong", "gambas", "timun", "ketimun", "selada", "seledri",
    "daun", "rebung", "genjer", "pakis", "paku", "taoge", "toge",
    "lobak", "pe-cay", "pecai", "caisin", "baligo", "kundur",
    "jantung pisang", "bunga pepaya", "bunga turi", "kembang turi",
    "kapri muda", "kool", "leunca", "tekokak", "kenikir",
    "kemangi", "katuk", "kelor", "singkong daun", "daun singkong",
    "rumput laut", "jamur", "sayur", "tumis bayam", "tumis kangkung",
    "capcai", "cap cai", "sop kool", "wortel", "tomat",
    "nangka muda", "pepaya muda", "labu siam", "labu air",
    "labu kuning", "labu waluh", "umbut",
    "bawang merah", "bawang putih", "bawang bombay",
    "cabai", "kunyit", "jahe", "serai", "lengkuas",
    "kecipir buah", "kecipir muda", "komak polong",
    "kacang panjang kukus", "kacang panjang tumis",
    "pelecing", "karedok", "gado-gado", "asinan",
    "sop", "lodeh",
]

KATEGORI_HEWANI = [
    "ayam", "sapi", "kambing", "domba", "babi", "kerbau", "kuda",
    "kelinci", "rusa", "bebek", "itik", "burung", "angsa", "belibis",
    "ikan", "udang", "cumi", "kepiting", "kerang", "rajungan",
    "belut", "lele", "bandeng", "baronang", "bawal", "cakalang",
    "gabus", "gurame", "kakap", "kembung", "layang", "lemuru",
    "mas ", "mujair", "nila", "patin", "salmon", "sardines", "sarden",
    "selar", "sepat", "teri", "tongkol", "tuna", "tenggiri",
    "daging", "hati", "ginjal", "otak", "usus", "babat",
    "telur", "kornet", "dendeng", "abon", "sosis",
    "keong", "kodok", "katak", "siput", "bekicot",
    "ham", "bacon", "rendang", "empal", "bulgogi",
    "rebon", "peda", "pindang", "jambal",
    "terasi", "petis", "bekasam", "bekasang", "rusip",
    "penyu", "kura-kura", "buaya",
]

KATEGORI_NABATI = [
    "tahu", "tempe", "oncom", "kacang hijau", "kacang merah",
    "kacang kedelai", "kacang tanah", "kacang bogor", "kacang gude",
    "kacang tolo", "kacang tunggak", "kacang arab",
    "kacang endel", "kacang ijo", "kacang komak",
    "kacang mete", "biji jambu mete",
    "kembang tahu", "susu kedelai",
    "koro", "koro benguk", "koro wedus",
    "lamtoro", "pete", "petai",
    "melinjo",
]

KATEGORI_KARBO = [
    "nasi", "beras", "ketan", "lontong", "ketupat",
    "singkong", "ubi", "talas", "kentang", "jagung",
    "mi ", "mie ", "bihun", "soun", "makaroni", "spaghetti",
    "roti", "tepung", "oat", "havermout",
    "sagu", "gaplek", "gadung", "ganyong", "uwi", "suweg",
    "sukun", "batatas", "tales",
    "bubur", "papeda", "pulut",
    "lemper", "lopis", "lupis",
    "misoa", "vermicelli",
    "tiwul", "oyek", "gatot",
    "beras merah", "beras hitam",
]

# ===========================================================
# 🚫 BLACKLIST — Makanan yang TIDAK boleh masuk rekomendasi
# (sama seperti di algoritma.py, plus tambahan)
# ===========================================================
BLACKLIST_KEYWORDS = [
    # Junk food, gorengan berat, snack
    "goreng", "crispy", "kerupuk", "keripik", "kripik", "emping",
    "rempeyek", "risoles", "pastel", "bakwan", "mendoan",
    "combro", "misro", "cireng", "cimol", "cilok",
    
    # Kue & dessert
    "kue", "cake", "dodol", "lapis", "bolu", "biskuit", "wafer",
    "permen", "coklat", "puding", "pudding", "getuk", "geplak",
    "jenang", "onde-onde", "klepon", "kelepon", "martabak",
    "bika", "wingko", "wajit", "yangko", "noga", "enting",
    "brem", "widaran", "japilus", "masekat",
    "bagea", "bangket", "semprong", "sus ", "talam",
    "apem", "bugis", "putu", "satu ", "lumpur",
    "ledre", "deblo", "brondong",
    
    # Minuman manis & olahan gula
    "sirup", "setrup", "madu", "gula", "melase", "es krim",
    "es mambo", "es sirup", "lemonade", "squash", "bir ",
    "kopi", "teh ", "coklat bubuk",
    
    # Minyak & lemak murni
    "minyak", "lemak babi", "lemak kerbau", "margarin", "mentega",
    
    # Santan & olahan santan
    "santan", "gulai", "opor", "rendang", "tongseng",
    "soto betawi",
    
    # Olahan instan
    "instan", "kaleng",
    
    # Fast food
    "burger", "pizza", "hotdog", "kebab",
    "fried chicken", "french fries",
    "nugget", "corndog",
    
    # Lainnya yang tidak sehat untuk diet
    "pilus", "koya", "intip goreng", "renggi",
    "cassavastick", "opak", "lanting",
    "kwaci", "susu kental manis",
    
    # Bahan baku mentah yang bukan makanan siap saji
    "gelatine", "ragi", "maizena",
    "tepung", # tepung bukan makanan siap makan
]


def kategorikan_makanan(nama):
    """
    Auto-assign kategori berdasarkan nama makanan.
    Prioritas: Karbo > Hewani > Nabati > Sayur > Buah > Lainnya
    """
    nama_lower = nama.lower()
    
    # --- FILTER: Blacklist dulu ---
    for keyword in BLACKLIST_KEYWORDS:
        if keyword in nama_lower:
            return "SKIP"
    
    # --- Cek Karbo ---
    for keyword in KATEGORI_KARBO:
        if keyword in nama_lower:
            return "Karbo"
    
    # --- Cek Hewani ---
    for keyword in KATEGORI_HEWANI:
        if keyword in nama_lower:
            return "Hewani"
    
    # --- Cek Nabati ---
    for keyword in KATEGORI_NABATI:
        if keyword in nama_lower:
            return "Nabati"
    
    # --- Cek Sayur ---
    for keyword in KATEGORI_SAYUR:
        if keyword in nama_lower:
            return "Sayur"
    
    # --- Cek Buah ---
    for keyword in KATEGORI_BUAH:
        if keyword in nama_lower:
            return "Buah"
    
    return "Lainnya"


def run_import():
    # 1. Koneksi ke database
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 2. Ambil nama makanan yang sudah ada di food_cache (hindari duplikat)
    cursor.execute("SELECT nama_makanan FROM food_cache")
    existing_names = set(row['nama_makanan'].lower().strip() for row in cursor.fetchall())
    print(f"📊 Data existing di food_cache: {len(existing_names)} item")
    
    # 3. Tentukan ID awal (mulai dari 60001 agar tidak bentrok)
    START_ID = 60001
    current_id = START_ID
    
    # 4. Baca CSV
    added = 0
    skipped_blacklist = 0
    skipped_lainnya = 0
    skipped_duplicate = 0
    skipped_bad_data = 0
    
    kategori_count = {
        'Karbo': 0, 'Hewani': 0, 'Nabati': 0,
        'Sayur': 0, 'Buah': 0, 'Lainnya': 0
    }
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                nama = row['name'].strip()
                kalori = float(row['calories'])
                protein = float(row['proteins'])
                lemak = float(row['fat'])
                karbo = float(row['carbohydrate'])
                
                # Skip jika kalori 0 atau terlalu tinggi (> 900)
                if kalori <= 0 or kalori > 800:
                    skipped_bad_data += 1
                    continue
                
                # Skip jika sudah ada duplikat
                if nama.lower().strip() in existing_names:
                    skipped_duplicate += 1
                    continue
                
                # Auto-kategorikan
                kategori = kategorikan_makanan(nama)
                
                if kategori == "SKIP":
                    skipped_blacklist += 1
                    continue
                
                if kategori == "Lainnya":
                    skipped_lainnya += 1
                    continue
                
                # Insert ke food_cache
                fatsecret_id = str(current_id)
                
                try:
                    cursor.execute("""
                        INSERT INTO food_cache 
                        (fatsecret_id, nama_makanan, kalori, protein, karbo, lemak, kategori)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (fatsecret_id, nama, kalori, protein, karbo, lemak, kategori))
                    
                    existing_names.add(nama.lower().strip())
                    current_id += 1
                    added += 1
                    kategori_count[kategori] += 1
                    
                except sqlite3.IntegrityError:
                    skipped_duplicate += 1
                    continue
                    
            except (ValueError, KeyError) as e:
                skipped_bad_data += 1
                continue
    
    conn.commit()
    
    # 5. Tampilkan Hasil
    print("\n" + "=" * 55)
    print("✅ IMPORT SELESAI!")
    print("=" * 55)
    print(f"   ➕ Berhasil ditambahkan  : {added} makanan")
    print(f"   🚫 Skip (blacklist)      : {skipped_blacklist}")
    print(f"   ⚠️  Skip (Lainnya)       : {skipped_lainnya}")
    print(f"   🔁 Skip (duplikat)       : {skipped_duplicate}")
    print(f"   ❌ Skip (data buruk)     : {skipped_bad_data}")
    print()
    print("📊 RINCIAN PER KATEGORI:")
    print("-" * 35)
    for kat, count in kategori_count.items():
        if count > 0:
            emoji = {"Karbo": "🍚", "Hewani": "🍗", "Nabati": "🫘", "Sayur": "🥬", "Buah": "🍎"}.get(kat, "📦")
            print(f"   {emoji} {kat:10s} : +{count}")
    
    # 6. Tampilkan total akhir
    cursor.execute("SELECT kategori, COUNT(*) as c FROM food_cache GROUP BY kategori")
    print("\n📈 TOTAL DATA food_cache SEKARANG:")
    print("-" * 35)
    for row in cursor.fetchall():
        print(f"   {row['kategori']:10s} : {row['c']}")
    
    total = cursor.execute("SELECT COUNT(*) FROM food_cache").fetchone()[0]
    print(f"\n   GRAND TOTAL: {total} makanan")
    
    conn.close()


if __name__ == "__main__":
    run_import()
