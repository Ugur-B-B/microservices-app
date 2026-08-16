from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Kendi yazdığımız dosyalardan import ediyoruz
from database import engine, SessionLocal, Base
from models import UserDB

# Uygulama ilk açıldığında, models.py'de tanımlı tabloları
# veritabanında otomatik oluşturuyor (eğer yoksa)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

# Pydantic modeli - API'ye gelen/giden JSON şeması
# (Bu, veritabanı modelinden (UserDB) ayrı - biri DB için, biri API için)
class User(BaseModel):
    id: int
    name: str
    email: str

    # Bu ayar, SQLAlchemy objelerini otomatik olarak
    # Pydantic modeline çevirebilmemizi sağlıyor
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

@app.get("/")
def read_root():
    return {"service": "user-service", "status": "running"}

# Tüm kullanıcıları veritabanından çekiyoruz
@app.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

# Yeni kullanıcıyı veritabanına kaydediyoruz
@app.post("/users", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this ID already exists")

    new_user = UserDB(id=user.id, name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user