# SQLAlchemy'nin temel bileşenlerini içeri aktarıyoruz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# os - işletim sisteminin ortam değişkenlerini (environment variables) okumak için
import os

# os.getenv("DATABASE_URL", "varsayılan_değer") -> önce DATABASE_URL adında
# bir ortam değişkeni var mı diye bakar, varsa onu kullanır.
# Yoksa (örneğin senin laptop'unda testler çalışırken), ikinci parametredeki
# varsayılan değeri (localhost) kullanır.
# Kubernetes'te bu değişkeni Deployment YAML'ından "user-postgres" olarak vereceğiz,
# böylece aynı kod hem yerelde hem Kubernetes'te sorunsuz çalışabilecek
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://berk:berk123@localhost:5432/userdb"
)

# Engine - SQLAlchemy'nin veritabanına gerçek bağlantıyı kurduğu motor
engine = create_engine(DATABASE_URL)

# Session - her istek için veritabanıyla konuşacağımız oturum
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - tüm tablo modellerimizin miras alacağı temel sınıf
Base = declarative_base()