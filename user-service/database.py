# SQLAlchemy'nin temel bileşenlerini içeri aktarıyoruz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Dikkat: artık "localhost" değil, Kubernetes Service ismini kullanıyoruz.
# "user-postgres" ismi, biraz önce yazdığımız user-postgres-service.yaml'daki
# metadata.name ile birebir aynı olmalı - Kubernetes bu ismi otomatik olarak
# doğru Pod'un IP adresine çevirir (buna "Service Discovery" denir)
DATABASE_URL = "postgresql+psycopg://berk:berk123@user-postgres:5432/userdb"

# Engine - SQLAlchemy'nin veritabanına gerçek bağlantıyı kurduğu motor
engine = create_engine(DATABASE_URL)

# Session - her istek için veritabanıyla konuşacağımız oturum
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - tüm tablo modellerimizin miras alacağı temel sınıf
Base = declarative_base()