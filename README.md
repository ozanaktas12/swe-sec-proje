# MiniShop — SQL Injection Korumalı E-Ticaret Arama Modülü

**SEN 2008 Software Security** dersi term projesi.

MiniShop, basit bir online elektronik mağazasıdır. Kullanıcılar ürün arayabilir. Projenin asıl odağı: **ürün arama modülündeki SQL Injection açığını göstermek ve korumak**.

---

## Yapay Zeka İçin Bağlam (AI'ya Bunu Ver)

> Bu repo 3 kişilik bir ekip projesidir. Herkes **kendi branch'inde** çalışır, `main`'e doğrudan push edilmez.
>
> - **Ozan** → `member/ozan` → `app.py` (SQL Injection, arama modülü, Secure/Vulnerable mod)
> - **Demir** → `member/demir` → `security/waf.py` (WAF, regex pattern tespiti)
> - **Arda** → `member/arda` → `security/auth.py`, `database.py` (login, bcrypt, loglama)
>
> `main` branch = hocaya sunulacak stabil versiyon. Biten işler Pull Request ile `main`'e merge edilir.
>
> Kurulum: `git clone` → `git checkout member/ISIM` → `venv` → `pip install -r requirements.txt` → `python app.py` → http://127.0.0.1:5000 (admin / Admin123!)

---

## Ekip Hızlı Özet — Ne Yapacağız?

### Adım 1: İlk Kurulum (Herkes Bir Kez)

```bash
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje

git checkout member/ozan      # Ozan
# git checkout member/demir   # Demir
# git checkout member/arda  # Arda

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Tarayıcı: **http://127.0.0.1:5000** — Giriş: `admin` / `Admin123!`

---

### Adım 2: Günlük Çalışma (Her Oturum)

```bash
git checkout member/SENIN-ISMIN     # kendi branch'ine geç
git pull origin main                # main'deki güncellemeleri al
source venv/bin/activate
python app.py                       # sunucuyu başlat

# → Kod yaz, tarayıcıda test et, kaydet...

git add .
git commit -m "Demir: ne yaptığını kısaca yaz"
git push
```

**Kural:** Herkes sadece kendi branch'inde çalışır. `main`'e doğrudan push etme.

---

### Adım 3: Main'e Birleştirme (Hazır Olunca)

1. GitHub → [swe-sec-proje](https://github.com/ozanaktas12/swe-sec-proje)
2. **Pull requests** → **New pull request**
3. Base: `main` ← Compare: `member/SENIN-ISMIN`
4. Ne yaptığını yaz → ekip review → **Merge**

---

### Kim Nerede Çalışır?

| Kişi | Branch | Dosya | Ne yapar |
|------|--------|-------|----------|
| Ozan | `member/ozan` | `app.py` | Arama modülü, Secure/Vulnerable mod |
| Demir | `member/demir` | `security/waf.py` | SQL injection pattern tespiti |
| Arda | `member/arda` | `security/auth.py`, `database.py` | Login, parola hash, loglar |

Detaylı rehber: **[EKIP_REHBERI.md](EKIP_REHBERI.md)** | Git kuralları: **[CONTRIBUTING.md](CONTRIBUTING.md)**

---

## Proje Özeti

Bu proje 3 ana parçadan oluşur:

1. **E-ticaret arayüzü** — Kullanıcı ürünleri görür ve arar (`/shop`)
2. **Güvenlik katmanı (WAF)** — Arama girdisini SQL injection pattern'lerine karşı kontrol eder (`security/waf.py`)
3. **Admin güvenlik paneli** — Mod değiştirme, loglar, demo payload'ları (`/admin/security`)

**İki mod:**
- **Secure Mode:** Parameterized query + WAF engeller
- **Vulnerable Mode:** String concatenation + WAF sadece loglar (demo için)

---

## Dosya Yapısı

```
├── app.py                  # Flask route'lar, arama mantığı, WAF middleware
├── config.py               # Secret key, DB yolu
├── database.py             # SQLite tabloları + seed data
├── security/
│   ├── auth.py             # Login/register (bcrypt)
│   └── waf.py              # SQL injection tespiti (regex)
├── templates/              # HTML sayfalar (shop, admin, login...)
└── static/css/style.css
```

`app.db` ilk `python app.py` çalıştırmasında otomatik oluşur.

---

## Sayfalar

| URL | Kim | Ne yapar |
|-----|-----|----------|
| `/shop` | Herkes | Ürün listesi + arama |
| `/admin/security` | Admin | Mod toggle, test payload'ları, loglar |
| `/admin/logs` | Admin | Tüm güvenlik olayları |

---

## SQL Injection — Kısa Özet

```python
# Savunmasız (Vulnerable Mode):
sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"

# Güvenli (Secure Mode):
db.execute("SELECT * FROM products WHERE name LIKE ?", [f"%{query}%"])
```

Test payload (Vulnerable Mode, arama kutusu): `' OR '1'='1`

---

## Demo Akışı (Sunum)

1. Admin giriş → mağazada "laptop" ara
2. Security Panel → Vulnerable Mode
3. `' OR '1'='1` → tüm ürünler gelir
4. Secure Mode → aynı saldırı engellenir
5. Security Logs → kayıtlar görünür

---

## Branch Yapısı

| Branch | Amaç |
|--------|------|
| `main` | Hocaya sunulacak ana proje — **dokunma, PR ile merge** |
| `develop` | Birleştirme test alanı |
| `member/ozan` | Ozan'ın çalışma alanı |
| `member/demir` | Demir'in çalışma alanı |
| `member/arda` | Arda'nın çalışma alanı |

---

## Sık Sorulan Sorunlar

| Sorun | Çözüm |
|-------|--------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Port 5000 meşgul | Terminali kapat veya `lsof -ti:5000 \| xargs kill -9` |
| Değişiklik görünmüyor | Ctrl+C → `python app.py` tekrar |
| DB bozuldu | `rm app.db` → `python app.py` |
| Yanlış branch | `git checkout member/SENIN-ISMIN` |

---

## Teknolojiler

Python 3 / Flask / SQLite / bcrypt / Bootstrap 5
