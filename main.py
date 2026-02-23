from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import models

# API Uygulamasını başlatıyoruz
app = FastAPI(title="Kişisel Finans API")

# Veri tabanına bağlanma fonksiyonu
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kullanıcıdan gelecek verilerin şablonu (Pydantic ile)
class CategoryCreate(BaseModel):
    name: str
    type: str

class TransactionCreate(BaseModel):
    amount: float
    description: str
    category_id: int

# --- API Uç Noktaları (Endpoints) ---

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Finans Takip Sistemine Hoş Geldiniz!"}

# Yeni kategori ekleme işlemi
@app.post("/kategori-ekle/")
def kategori_ekle(kategori: CategoryCreate, db: Session = Depends(get_db)):
    yeni_kategori = models.Category(name=kategori.name, type=kategori.type)
    db.add(yeni_kategori)
    db.commit()
    db.refresh(yeni_kategori)
    return yeni_kategori


# Yeni işlem (harcama/gelir) ekleme
@app.post("/islem-ekle/")
def islem_ekle(islem: TransactionCreate, db: Session = Depends(get_db)):
    yeni_islem = models.Transaction(
        amount=islem.amount,
        description=islem.description,
        category_id=islem.category_id
    )
    db.add(yeni_islem)
    db.commit()
    db.refresh(yeni_islem)
    return yeni_islem

# Tüm işlemleri listeleme
@app.get("/islemler/")
def islemleri_getir(db: Session = Depends(get_db)):
    islemler = db.query(models.Transaction).all()
    return islemler