from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

# 1. Veri tabanı motorunu kuruyoruz
engine = create_engine('sqlite:///finance.db', echo=True)
Base = declarative_base()


# 2. Kategori tablosunu tanımlıyoruz (Maaş, Market vb.)
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="category")


# 3. İşlem tablosunu tanımlıyoruz (Harcamalar ve Gelirler)
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, default=date.today)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="transactions")


# 4. Tabloları oluşturuyoruz
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)