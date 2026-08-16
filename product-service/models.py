# Sütun tiplerini içeri aktarıyoruz
# Integer = tam sayı, String = metin, Float = ondalıklı sayı (fiyat için)
from sqlalchemy import Column,Integer,String,Float
# database.py'de tanımladığımız Base sınıfını alıyoruz
from database import Base
# Bu class, veritabanındaki "products" tablosunu temsil ediyor
# Python'da bir class yazıyoruz ama aslında bu, SQL'de
# "CREATE TABLE products (...)" komutunun karşılığı
class ProductDB(Base):
    # Tablo adı
    __tablename__ = "products"
    # Sütunlar
    id = Column(Integer, primary_key=True, index=True)  # id sütunu, birincil anahtar
    name = Column(String, nullable=False)                   # name sütunu, metin
    price = Column(Float, nullable=False)         
    stock = Column(Integer, nullable=False)             # stock sütunu, tam sayı