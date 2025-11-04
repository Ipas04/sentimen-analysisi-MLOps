from google_play_scraper import reviews_all, Sort
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Daftar ID aplikasi yang ingin di-scrape
app_ids = [
    'com.bca',
    'src.com.bni',
    'id.co.bri.brimo',
    'com.bsm.activity2'  
]

# Fungsi untuk scraping ulasan untuk setiap aplikasi
def scrape_reviews(app_id):
    try:
        print(f"Scraping review dari {app_id}...")
        reviews = reviews_all(
            app_id,
            lang='id',
            country='id',
            sort=Sort.MOST_RELEVANT,
            count=1000
        )

        # Tambahkan kolom app_id dan tanggal ulasan
        for review in reviews:
            review['app_id'] = app_id
            review['review_date'] = review['at']  # Menyimpan tanggal ulasan

        return reviews
    except Exception as e:
        print(f"Terjadi kesalahan saat scraping {app_id}: {e}")
        return []

# Gunakan ThreadPoolExecutor untuk mengambil data lebih cepat
all_reviews = []

with ThreadPoolExecutor() as executor:
    results = executor.map(scrape_reviews, app_ids)
    for result in results:
        all_reviews.extend(result)

# Convert ke DataFrame
df = pd.DataFrame(all_reviews)

# Simpan ke file CSV (opsional)
df.to_csv('all_app_reviews.csv', index=False)

print("✅ Selesai scraping semua aplikasi!")

