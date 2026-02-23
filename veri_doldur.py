import sqlite3
from datetime import date, timedelta

# Veritabanına bağlan
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Kategorileri garantiye alalım (Daha önce eklemediysen diye)
kategoriler = [
    (1, 'Maaş', 'gelir'),
    (2, 'Market', 'gider'),
    (3, 'Kira', 'gider'),
    (4, 'Akaryakıt', 'gider')
]
cursor.executemany("INSERT OR IGNORE INTO categories (id, name, type) VALUES (?, ?, ?)", kategoriler)

# Gerçekçi harcama ve gelir verileri (Ocak ve Şubat ayları için)
islemler = [
    (45000.0, '2026-01-01', 'Ocak Maaşı', 1),
    (15000.0, '2026-01-05', 'Ocak Kirası', 3),
    (2500.0, '2026-01-10', 'Haftalık Market', 2),
    (1200.0, '2026-01-15', 'Benzin Alımı', 4),
    (3000.0, '2026-01-22', 'Büyük Market Alışverişi', 2),
    (45000.0, '2026-02-01', 'Şubat Maaşı', 1),
    (15000.0, '2026-02-05', 'Şubat Kirası', 3),
    (2800.0, '2026-02-12', 'Haftalık Market', 2),
    (1500.0, '2026-02-18', 'Benzin Alımı', 4)
]

# İşlemleri tabloya yaz
cursor.executemany("INSERT INTO transactions (amount, date, description, category_id) VALUES (?, ?, ?, ?)", islemler)

conn.commit()
conn.close()

print("✅ 2 aylık simülasyon verisi veri tabanına başarıyla eklendi!")