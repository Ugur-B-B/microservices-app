# SQLAlchemy'nin temel bileşenlerini içeri aktarıyoruz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# Veritabanı bağlantı adresi (connection string)
# Format: postgresql+psycopg://kullanici:sifre@host:port/veritabani_adi
# Dikkat: port 5433 kullanıyoruz çünkü product-postgres container'ını
# host makinenin 5433 portuna yönlendirmiştik (user-postgres zaten 5432'yi kullanıyor)
DATABASE_URL = "postgresql+psycopg://berk:berk123@product-postgres:5432/productdb"
# Engine - SQLAlchemy'nin veritabanına gerçek bağlantıyı kurduğu "motor"
# Bu, henüz bağlantıyı açmıyor, sadece "nasıl bağlanacağını" biliyor
engine=create_engine(DATABASE_URL)

# Session - her API isteği için veritabanıyla açacağımız "oturum"
# Her istek geldiğinde yeni bir session açılır, iş bitince kapanır
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
# Base - tüm tablo modellerimizin (models.py'deki class'ların) 
# miras alacağı temel sınıf. SQLAlchemy bu sayede hangi class'ların
# birer veritabanı tablosu olduğunu anlar
Base=declarative_base()