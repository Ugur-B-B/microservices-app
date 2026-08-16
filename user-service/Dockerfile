# Küçük ve hızlı bir Python image'ı kullanıyoruz
FROM python:3.12.0-slim

# Container içinde çalışma dizinini belirliyoruz
WORKDIR /app

# Önce sadece requirements.txt'yi kopyalıyoruz
# (Docker cache mantığı: kod değişse bile bağımlılıklar değişmediyse
# bu adım tekrar çalışmaz, build daha hızlı olur)
COPY requirements.txt .

# Bağımlılıkları kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Şimdi geri kalan kodu kopyalıyoruz
COPY . .

# Servisin dışarıya açacağı port
EXPOSE 8000

# Container ayağa kalktığında çalışacak komut
# uvicorn ile FastAPI uygulamasını başlatıyoruz, tüm network arayüzlerinden erişilebilir yapıyoruz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
