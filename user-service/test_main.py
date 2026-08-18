# FastAPI'nin test aracı - gerçek bir sunucu başlatmadan,
# API'ye "sahte" istekler göndermemizi sağlıyor
from fastapi.testclient import TestClient
# main.py'deki FastAPI uygulamamızı içeri alıyoruz
from main import app

# TestClient'ı uygulamamıza bağlıyoruz - artık bu "client" üzerinden
# GET, POST gibi istekler gönderebiliriz
client = TestClient(app)

# Her test fonksiyonu "test_" ile BAŞLAMALI - pytest bu ismi görüp
# otomatik olarak bunun bir test olduğunu anlıyor

def test_read_root():
    # "/" adresine sahte bir GET isteği gönderiyoruz
    response = client.get("/")
    # assert - "bunun doğru olduğunu iddia ediyorum" demek
    # Eğer status_code 200 değilse, test BAŞARISIZ (fail) olur
    assert response.status_code == 200
    # Dönen JSON'un içinde "status": "running" olduğunu kontrol ediyoruz
    assert response.json()["status"] == "running"

def test_get_users_returns_list():
    # "/users" adresine GET isteği gönderiyoruz
    response = client.get("/users")
    # Status code 200 mü (başarılı mı) kontrol ediyoruz
    assert response.status_code == 200
    # Dönen cevabın bir liste (list) olduğunu kontrol ediyoruz
    # (çünkü /users her zaman bir kullanıcı listesi döndürmeli)
    assert isinstance(response.json(), list)

def test_get_nonexistent_user_returns_404():
    # Var olmayan bir id (999999) ile kullanıcı istiyoruz
    response = client.get("/users/999999")
    # Böyle bir kullanıcı olmadığı için 404 (bulunamadı) dönmesini bekliyoruz
    assert response.status_code == 404