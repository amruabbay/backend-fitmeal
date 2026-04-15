import sqlite3
import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Pastikan file algoritma.py ada di satu folder
from algoritma import DB_NAME, jalankan_algoritma

# ==========================================
# ⚠️ KUNCI FATSECRET (OAUTH 2.0)
# ==========================================
CLIENT_ID = "3539cf685adc4153b5d9b5fa48cbe582"
CLIENT_SECRET = "2f111c0b7f8c4eb393148ec5f543c610"

app = FastAPI()

# ==========================================
# 🔥 IZIN CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODEL DATA ---
class UserData(BaseModel):
    berat: float
    tinggi: float
    umur: int
    gender: str
    goal: str
    activity: str

# --- AUTHENTICATION ---
def dapatkan_token_oauth2():
    try:
        url = "https://oauth.fatsecret.com/connect/token"
        payload = {'grant_type': 'client_credentials', 'scope': 'premier'}
        response = requests.post(url, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
        if response.status_code == 200:
            return response.json().get('access_token')
    except:
        pass
    return None

# --- FUNGSI BULK (SCAN LEBIH BANYAK) ---
def cari_di_fatsecret_bulk(query):
    token = dapatkan_token_oauth2()
    if not token: return []

    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {'Authorization': f'Bearer {token}'}
    
    hasil_bulk = []
    
    # Kita ambil cukup banyak data di awal agar pagination lancar
    max_scan_pages = 3 

    try:
        for api_page in range(max_scan_pages):
            params = {
                "method": "foods.search",
                "search_expression": query,
                "format": "json",
                "max_results": 50,
                "page_number": api_page,
                "region": "ID",        # Filter ke database Indonesia
                "language": "id"       # Bahasa Indonesia
            }
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                foods = data.get("foods", {}).get("food", [])
                if isinstance(foods, dict): foods = [foods]
                if not foods: break 
                
                for item in foods:
                    # Ambil data mentah
                    nama = item.get('food_name', '')
                    brand = item.get('brand_name', '')
                    desc = item.get('food_description', '')
                    
                    # Filter sederhana
                    teks_lengkap = (nama + " " + brand).lower()
                    kata_kunci = query.lower().split()
                    
                    is_relevant = False
                    matches = 0
                    for k in kata_kunci:
                        if k in teks_lengkap: matches += 1
                    
                    if len(kata_kunci) == 1:
                        if matches >= 1: is_relevant = True
                    else:
                        if matches >= 1: is_relevant = True 

                    if is_relevant:
                        makanan = {
                            "id": int(item['food_id']),
                            "nama_makanan": f"{nama} ({brand})" if brand else nama,
                            "kalori": 0, "protein": 0, "karbo": 0, "lemak": 0,
                            "sumber": "api"
                        }
                        try:
                            if 'Calories:' in desc:
                                makanan['kalori'] = float(desc.split('Calories: ')[1].split('kcal')[0])
                            if 'Protein:' in desc:
                                makanan['protein'] = float(desc.split('Protein: ')[1].split('g')[0])
                            if 'Carbs:' in desc:
                                makanan['karbo'] = float(desc.split('Carbs: ')[1].split('g')[0])
                            if 'Fat:' in desc:
                                makanan['lemak'] = float(desc.split('Fat: ')[1].split('g')[0])
                        except: pass
                        hasil_bulk.append(makanan)
            else: break
        return hasil_bulk
    except: return []

# --- LOGIKA HITUNG KALORI ---
def hitung_kalori_user(data: UserData):
    if data.gender.lower() == "pria":
        bmr = (10 * data.berat) + (6.25 * data.tinggi) - (5 * data.umur) + 5
    else:
        bmr = (10 * data.berat) + (6.25 * data.tinggi) - (5 * data.umur) - 161
    
    faktor = 1.2
    if data.activity == "moderate": faktor = 1.55
    elif data.activity == "active": faktor = 1.725
    
    tdee = bmr * faktor
    
    if data.goal == "cutting": 
        target = tdee - 500
        protein_ratio = 150
    elif data.goal == "bulking": 
        target = tdee + 400
        protein_ratio = 130
    else: 
        target = tdee
        protein_ratio = 100
        
    return target, protein_ratio

# --- ENDPOINT REKOMENDASI ---
@app.post("/rekomendasi")
def get_rekomendasi(user: UserData):
    target_kalori, target_protein = hitung_kalori_user(user)
    menu_terbaik, stats = jalankan_algoritma(target_kalori, target_protein)
    
    if not menu_terbaik: 
        raise HTTPException(status_code=404, detail="Gagal generate menu.")
        
    return {
        "status": "success", 
        "user_info": {
            "target_kalori": round(target_kalori), 
            "target_protein": target_protein
        }, 
        "hasil_generasi": stats, 
        "menu": menu_terbaik
    }

# --- FUNGSI SCORING RELEVANSI PENCARIAN ---
def hitung_skor_relevansi(nama_makanan: str, query: str) -> int:
    """
    Menghitung skor relevansi sebuah makanan terhadap kata kunci pencarian.
    Skor LEBIH TINGGI = LEBIH RELEVAN (ditampilkan lebih atas).
    
    Sistem Poin:
    - Nama persis sama dengan query          → +1000
    - Nama diawali dengan query              → +500
    - Semua kata kunci ada di nama            → +200
    - Setiap kata kunci yang cocok            → +50
    - Kata kunci muncul sebagai kata utuh     → +30 per kata
    - Posisi kata kunci lebih awal di nama    → +20
    - Nama lebih pendek (lebih spesifik)      → +10
    """
    nama_lower = nama_makanan.lower().strip()
    query_lower = query.lower().strip()
    keywords = query_lower.split()
    
    skor = 0
    
    # 1. EXACT MATCH — nama persis sama
    if nama_lower == query_lower:
        skor += 1000
    
    # 2. STARTS WITH — nama diawali query lengkap
    if nama_lower.startswith(query_lower):
        skor += 500
    
    # 3. ALL KEYWORDS MATCH — semua kata kunci ada
    matches = sum(1 for k in keywords if k in nama_lower)
    if matches == len(keywords):
        skor += 200
    
    # 4. PER-KEYWORD MATCH — setiap kata yang cocok
    skor += matches * 50
    
    # 5. WHOLE WORD MATCH — kata kunci muncul sebagai kata utuh
    nama_words = nama_lower.split()
    for k in keywords:
        if k in nama_words:
            skor += 30
    
    # 6. POSISI AWAL — kata kunci muncul di awal nama
    for k in keywords:
        pos = nama_lower.find(k)
        if pos >= 0 and pos < 5:  # Muncul di 5 karakter pertama
            skor += 20
    
    # 7. NAMA PENDEK BONUS — nama yang lebih pendek biasanya lebih spesifik
    if len(nama_lower) < 25:
        skor += 10
    
    return skor

# --- ENDPOINT SEARCH (SERVER SIDE PAGINATION) ---
@app.get("/search")
def cari_makanan(
    q: str = "", 
    page: int = Query(0, ge=0),    # Halaman (0, 1, 2...)
    limit: int = Query(7, le=50)   # Jumlah item per load (Default 7)
):
    if not q: 
        return {"status": "success", "results": [], "has_next": False}

    # 1. AMBIL DATABASE LOKAL
    local_results = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM food_cache")
        all_local = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        keywords = q.lower().split()
        for item in all_local:
            nama_db = item['nama_makanan'].lower()
            if any(k in nama_db for k in keywords):
                local_results.append({
                    "id": int(item['fatsecret_id']),
                    "nama_makanan": item['nama_makanan'],
                    "kalori": float(item['kalori']), 
                    "protein": float(item['protein']),
                    "karbo": float(item['karbo']), 
                    "lemak": float(item['lemak']),
                    "sumber": "lokal"
                })
    except Exception as e:
        print(f"Error DB Lokal: {e}")

    # 2. AMBIL DARI API (Bulk Fetch)
    api_results = cari_di_fatsecret_bulk(q)
    
    # 3. GABUNGKAN SEMUA HASIL
    master_list = local_results + api_results
    
    # 4. URUTKAN BERDASARKAN SKOR RELEVANSI (TINGGI → RENDAH)
    master_list.sort(
        key=lambda item: hitung_skor_relevansi(item['nama_makanan'], q),
        reverse=True
    )
    
    # 5. POTONG DATA (SLICING) SESUAI PAGE & LIMIT
    start_index = page * limit
    end_index = start_index + limit
    
    final_results = []
    has_next = False

    if len(master_list) > start_index:
        final_results = master_list[start_index:end_index]
        has_next = len(master_list) > end_index
    
    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total_found": len(master_list),
        "results": final_results,
        "has_next": has_next
    }

@app.get("/")
def read_root(): 
    return {"message": "Server Ready", "cors": "enabled"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)