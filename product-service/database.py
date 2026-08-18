from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# os - ortam değişkenlerini okumak için
import os

# DATABASE_URL ortam değişkeni varsa onu kullan, yoksa localhost'a düş
# (Kubernetes'te bu değişkeni "product-postgres" olarak vereceğiz)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://berk:berk123@localhost:5433/productdb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()