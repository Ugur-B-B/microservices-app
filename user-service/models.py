# Sütun tiplerini içeri aktarıyoruz
from sqlalchemy import Column, Integer, String
# database.py'den Base sınıfını alıyoruz
from database import Base

# Bu class, veritabanındaki "users" tablosunu temsil ediyor
class UserDB(Base):
    __tablename__ = "users"

    # primary_key=True -> bu sütun benzersiz kimlik (id)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # unique=True -> aynı email iki kere kayıt olamaz
    email = Column(String, unique=True, nullable=False)