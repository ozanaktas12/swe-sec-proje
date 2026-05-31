# MiniShop — SQL Injection Korumalı E-Ticaret Arama Modülü

**SEN 2008 Software Security** dersi term projesi.

MiniShop, basit bir online elektronik mağazasıdır. Kullanıcılar ürün arayabilir. Projenin asıl odağı: **ürün arama modülündeki SQL Injection açığını göstermek ve korumak**.

---

## Proje Özeti (Yapay Zekaya Verirken Bunu Okut)

Bu proje 3 ana parçadan oluşur:

1. **E-ticaret arayüzü** — Kullanıcı ürünleri görür ve arar (`/shop`)
2. **Güvenlik katmanı (WAF)** — Arama kutusuna yazılan girdiyi SQL injection pattern'lerine karşı kontrol eder (`security/waf.py`)
3. **Admin güvenlik paneli** — Mod değiştirme, loglar, demo payload'ları (`/admin/security`)

**İki mod vardır:**
- **Secure Mode:** Parameterized query kullanılır + WAF saldırıları engeller
- **Vulnerable Mode:** String concatenation kullanılır (bilinçli olarak güvensiz) + WAF sadece loglar, engellemez

---

## Dosya Yapısı

```
software_sec_proj/
├── app.py                  # Ana Flask uygulaması — route'lar, arama mantığı, WAF middleware
├── config.py               # SECRET_KEY, veritabanı yolu
├── database.py             # SQLite tabloları (users, products, security_logs) + seed data
├── requirements.txt        # Flask, bcrypt
├── security/
│   ├── auth.py             # Login/register — bcrypt ile parola hashleme
│   └── waf.py              # SQL injection tespit motoru (regex pattern matching)
├── templates/
│   ├── shop.html           # Ana mağaza sayfası — ürün kartları + arama
│   ├── admin_security.html # Admin güvenlik paneli
│   ├── security_logs.html# Tüm güvenlik logları
│   ├── login.html / register.html / blocked.html / base.html
└── static/css/style.css    # Dark theme stiller
```

**Not:** `app.db` dosyası ilk çalıştırmada otomatik oluşur (`database.py` → `init_db()`). Repoya dahil değildir.

---

## Kurulum (Arkadaşlar İçin)

```bash
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Tarayıcıda: **http://127.0.0.1:5000**

**Demo hesap:** `admin` / `Admin123!`

---

## Sayfalar

| URL | Kim görür | Ne yapar |
|-----|-----------|----------|
| `/shop` | Herkes | Ürün listesi + arama |
| `/admin/security` | Sadece admin | Secure/Vulnerable mod toggle, test payload'ları, son loglar |
| `/admin/logs` | Sadece admin | Tüm güvenlik olayları |

Normal kullanıcı sadece mağazayı görür. Güvenlik özellikleri admin panelindedir.

---

## SQL Injection Nasıl Çalışıyor?

### Savunmasız kod (Vulnerable Mode):
```python
sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
db.execute(sql)
```
Kullanıcı `' OR '1'='1` yazarsa → tüm ürünler döner.

### Güvenli kod (Secure Mode):
```python
sql = "SELECT * FROM products WHERE name LIKE ?"
db.execute(sql, [f"%{query}%"])
```
Kullanıcı ne yazarsa yazsın → sadece metin olarak aranır, SQL komutu olmaz.

---

## Demo / Sunum Akışı

1. `admin` / `Admin123!` ile giriş yap
2. Mağazada "laptop" ara → normal sonuçlar
3. **Security Panel** → Vulnerable Mode'a geç
4. Arama kutusuna `' OR '1'='1` yaz → tüm ürünler gelir (injection çalışır)
5. `' UNION SELECT 1,username,password_hash,4,5,6 FROM users--` → kullanıcı hash'leri görünür
6. Secure Mode'a geri dön → aynı saldırılar engellenir
7. **Security Logs** → olaylar kayıtlı

---

## Test Payload'ları

Vulnerable Mode'dayken `/shop` arama kutusuna yaz:

| Saldırı | Payload |
|---------|---------|
| Tüm verileri çek | `' OR '1'='1` |
| Kullanıcı parolalarını çal | `' UNION SELECT 1,username,password_hash,4,5,6 FROM users--` |
| Tablo yapısını öğren | `' UNION SELECT 1,name,sql,4,5,6 FROM sqlite_master WHERE type='table'--` |

---

## 3 Kişilik Ekip Rolleri

| Kişi | Konu | Okuması gereken dosya |
|------|------|----------------------|
| 1 | SQL Injection + Secure/Vulnerable mod | `app.py` → `_search_products()` |
| 2 | WAF tespit motoru | `security/waf.py`, `before_request_hook()` |
| 3 | Auth + loglama + veritabanı | `security/auth.py`, `database.py` |

---

## Teknolojiler

- **Python 3 / Flask** — Web sunucusu
- **SQLite** — Veritabanı (kurulum gerektirmez, tek dosya)
- **bcrypt** — Parola hashleme
- **Bootstrap 5** — Arayüz

---

## Sık Sorulan Sorular

**S: app.db nerede?**  
C: `python app.py` çalıştırınca otomatik oluşur. Silersen tekrar oluşur (loglar sıfırlanır).

**S: Normal kullanıcı Security Panel'i görür mü?**  
C: Hayır, sadece `role=admin` olan kullanıcı görür.

**S: WAF ne zaman engeller?**  
C: Secure Mode açıkken, arama kutusuna bilinen SQL injection pattern'i yazılırsa.

**S: Vulnerable Mode ne işe yarar?**  
C: Saldırının gerçekten çalıştığını göstermek için. Sunumda Secure vs Vulnerable karşılaştırması yapılır.
