import pandas as pd
import sqlite3
import warnings

warnings.filterwarnings("ignore") # Gereksiz pandas uyarılarını gizle

# 1. Veri tabanına bağlan
conn = sqlite3.connect('finance.db')

# 2. SQL sorgusu ile işlemleri ve kategori isimlerini birleştirerek çek
sorgu = """
SELECT t.date, t.amount, t.description, c.name as category, c.type 
FROM transactions t
JOIN categories c ON t.category_id = c.id
"""

# 3. Veriyi Pandas DataFrame'ine aktar (İşte 'df' burada hayat buluyor!)
df = pd.read_sql_query(sorgu, conn)

# 4. Veri tabanı bağlantısını kapat
conn.close()

# --- BÖLÜM 1: TEMEL ANALİZ ---
print("--- Tüm Hareketler ---")
print(df)

# Gelir ve gider toplamlarını hesapla
ozet = df.groupby('type')['amount'].sum()
print("\n--- Finansal Özet ---")
print(ozet)

# --- BÖLÜM 2: EKONOMETRİK HARCAMA TRENDİ VE TAHMİN MODELİ ---
print("\n--- Ekonometrik Harcama Trendi ve Tahmin Modeli ---")

# Sadece "gider" olan işlemleri filtrele
giderler = df[df['type'] == 'gider'].copy()

# Tarih sütununu gerçek bir zaman serisi formatına çevir
giderler['date'] = pd.to_datetime(giderler['date'])

# Veriyi tarihe göre grupla ve günlük toplam harcamaları bul
gunluk_gider = giderler.groupby('date')['amount'].sum().reset_index()
gunluk_gider.set_index('date', inplace=True)

# Günlük düzensiz verileri 'Haftalık' (W) periyotlara toplayarak daha anlamlı bir trend elde et
haftalik_gider = gunluk_gider.resample('W').sum()

# Basit Üstel Düzeltme (Exponential Smoothing) uygulayarak trendi yumuşat
# alpha=0.5 katsayısı ile yakın zamandaki harcamalara %50, geçmiş harcamalara %50 ağırlık verilir.
haftalik_gider['Trend_Tahmini'] = haftalik_gider['amount'].ewm(alpha=0.5, adjust=False).mean()

# Görüntüyü güzelleştirmek için küsuratları yuvarla
haftalik_gider = haftalik_gider.round(2)

print("\nHaftalık Gerçekleşen Giderler ve Gelecek Trendi:")
print(haftalik_gider)
print("\nNot: 'Trend_Tahmini' sütunu, geçmiş harcama şoklarını yumuşatarak bir sonraki periyot için beklenen harcama seviyesini gösterir.")