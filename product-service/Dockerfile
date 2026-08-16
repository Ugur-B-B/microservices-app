FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# Not: port 8001 kullanıyoruz çünkü user-service zaten 8000'de çalışıyor
# İki servisi aynı anda yerelde test edebilmek için farklı portlar gerekiyor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
