# FastAPI framework'ünü içeri aktarıyoruz
# Depends -> "bağımlılık enjeksiyonu" (dependency injection) için,
# her istekte otomatik olarak veritabanı bağlantısı sağlayacak
from fastapi import FastAPI, HTTPException, Depends
# Pydantic - API'ye gelen/giden JSON şeması için
from pydantic import BaseModel
# SQLAlchemy'nin Session tipini alıyoruz (veritabanı oturumu)
from sqlalchemy.orm import Session

# Kendi yazdığımız dosyalardan gerekli parçaları içeri alıyoruz
from database import engine, SessionLocal, Base
from models import ProductDB

# Uygulama açılırken, models.py'de tanımlı "products" tablosunu
# veritabanında otomatik oluşturuyor (eğer daha önce oluşmadıysa)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")

# Pydantic modeli - bu, API'ye giren/çıkan JSON'un şeklini tanımlıyor
# Not: Bu, models.py'deki ProductDB'den FARKLI bir şey.
# ProductDB -> veritabanı tablosu ne şekilde olacak
# Product (aşağıdaki) -> API'ye gelen/giden veri ne şekilde olacak
# İkisi genelde birbirine benzer ama farklı amaçlar için var
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    # Bu ayar, SQLAlchemy'den gelen veritabanı objesini (ProductDB)
    # otomatik olarak bu Pydantic modeline (Product) çevirebilmemizi sağlıyor
    class Config:
        from_attributes = True

# Her istek için veritabanı oturumu (session) açıp,