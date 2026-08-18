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
# istek bittiğinde otomatik kapatan yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint - servis ayakta mı diye kontrol etmek için
@app.get("/")
def read_root():
    return {"service": "product-service", "status": "running"}

# Tüm ürünleri veritabanından çekiyoruz
@app.get("/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

# Yeni ürünü veritabanına kaydediyoruz
@app.post("/products", response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    # Aynı id'de ürün var mı diye kontrol
    existing = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    # Pydantic modelinden (Product) veritabanı objesi (ProductDB) oluşturuyoruz
    new_product = ProductDB(
        id=product.id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )
    db.add(new_product)      # değişikliği oturuma ekle
    db.commit()               # değişikliği veritabanına kalıcı olarak yaz
    db.refresh(new_product)   # veritabanından güncel halini geri çek
    return new_product

# Tek bir ürünü id'ye göre getiren endpoint
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Stok azaltan endpoint - örnek bir "sipariş verildi" senaryosu
@app.patch("/products/{product_id}/reduce-stock")
def reduce_stock(product_id: int, amount: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < amount:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    product.stock -= amount   # stoktan düş
    db.commit()                # veritabanına kalıcı olarak yaz
    db.refresh(product)        # güncel halini geri çek
    return product