# Ekip Rehberi — Adım Adım Yol Haritası

Herkes kendi branch'inde çalışır. Bitince Pull Request ile `main`'e birleştiririz.

---

## Özet: 3 Aşama

| Aşama | Ne yapılır | Ne zaman |
|-------|------------|----------|
| **1. Kurulum** | Clone, branch seç, venv, çalıştır | İlk gün, bir kez |
| **2. Çalışma** | Kod yaz, test et, commit, push | Her oturum |
| **3. Birleştirme** | Pull Request aç → review → merge | İş bitince |

---

## Aşama 1 — İlk Kurulum

```bash
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje

git checkout member/demir     # kendi adını yaz: ozan / demir / arda

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

- Tarayıcı: http://127.0.0.1:5000
- Giriş: `admin` / `Admin123!`
- İlk test: mağazada "laptop" ara, sonuç gelsin

---

## Aşama 2 — Günlük Çalışma

Her çalışma oturumunda sırayla:

```bash
# 1. Kendi branch'ine geç
git checkout member/demir

# 2. Main'deki güncellemeleri al (başkası merge ettiyse)
git pull origin main

# 3. Sunucuyu başlat
source venv/bin/activate
python app.py

# 4. Kod yaz → tarayıcıda test et → kaydet

# 5. Git'e gönder
git add .
git commit -m "Demir: WAF'a yeni pattern eklendi"
git push
```

### İlk Deneme (Herkes Yapsın)

1. `templates/shop.html` aç
2. "Welcome to MiniShop" yazısını değiştir
3. Tarayıcıyı yenile — değişikliği gör
4. Commit + push yap

Bu çalışıyorsa kurulum tamam.

---

## Aşama 3 — Main'e Birleştirme

**Kimse `main`'e doğrudan push etmesin.**

1. GitHub → https://github.com/ozanaktas12/swe-sec-proje
2. **Pull requests** → **New pull request**
3. Base: `main` ← Compare: `member/demir`
4. Başlık + açıklama yaz
5. Ozan veya Arda review eder → **Merge pull request**

---

## Kişiye Göre Çalışma Alanı

### Ozan — `member/ozan` — `app.py`

- `_search_products()` fonksiyonu — Secure vs Vulnerable SQL mantığı
- Yeni route ekleme, arama filtreleri
- Test: Vulnerable Mode → `' OR '1'='1` → tüm ürünler gelmeli

### Demir — `member/demir` — `security/waf.py`

- `SQL_INJECTION_PATTERNS` listesi — regex kuralları
- Yeni pattern ekleme / test etme
- Test: Secure Mode → saldırı payload'u → 403 Blocked

### Arda — `member/arda` — `security/auth.py`, `database.py`

- Login/register, bcrypt hashleme
- Ürün seed data, security log kayıtları
- Test: yanlış parola → Security Panel'de AUTH_FAILURE logu

---

## Yapay Zekaya Sorarken

1. README.md'yi context olarak ver
2. Kendi dosyanı ekle
3. Net sor:

> "MiniShop projesinde `security/waf.py` dosyasına time-based blind SQL injection için yeni bir regex pattern ekle."

---

## Kurallar

- ✅ Kendi branch'inde çalış
- ✅ Kendi dosyalarında değişiklik yap
- ✅ Commit mesajında adını yaz: `Demir: ...`
- ✅ Bitince Pull Request aç
- ❌ `main`'e doğrudan push etme
- ❌ Başkasının dosyasına sormadan dokunma

---

## Sorun Giderme

| Sorun | Çözüm |
|-------|--------|
| Flask bulunamadı | `pip install -r requirements.txt` |
| Port meşgul | Eski terminali kapat |
| Push reddedildi | `git pull origin main` sonra tekrar push |
| app.db bozuldu | `rm app.db && python app.py` |

---

## Checklist

- [ ] Repoyu clone ettim
- [ ] Kendi branch'ime geçtim (`member/ozan` / `demir` / `arda`)
- [ ] `python app.py` çalışıyor
- [ ] Admin ile giriş yaptım
- [ ] Küçük bir değişiklik yaptım ve gördüm
- [ ] `git commit` + `git push` yaptım
- [ ] Kendi dosyamı okudum
- [ ] Vulnerable + Secure mod farkını denedim
