# Ekip Git Workflow

Bu repoda herkes kendi branch'inde çalışır, bitince `main`'e birleştiririz.

## Branch Yapısı

```
main                  ← Ana proje (hocaya sunulacak, stabil versiyon)
develop               ← Entegrasyon (birleştirme test alanı)
member/ozan           ← Ozan — SQL Injection + arama modülü
member/demir          ← Demir — WAF tespit motoru
member/arda           ← Arda — Auth + loglama
```

**Kural:** Kimse doğrudan `main`'e push etmesin. Önce kendi branch'inde çalış, sonra Pull Request aç.

---

## İlk Kurulum (Herkes Bir Kez)

```bash
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Kendi Branch'ine Geçme

Branch'ler zaten oluşturuldu. Sadece checkout yap:

```bash
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje
git checkout member/demir    # veya member/arda, member/ozan
```

---

## Günlük Çalışma

```bash
# Kendi branch'ine geç
git checkout member/SENIN-ISMIN

# Kod yaz, test et...

git add .
git commit -m "Demir: WAF pattern listesine yeni kural eklendi"
git push
```

---

## Main'e Birleştirme (Pull Request)

1. GitHub'da repoya git: https://github.com/ozanaktas12/swe-sec-proje
2. **Pull requests** → **New pull request**
3. Base: `main` ← Compare: `member/SENIN-ISMIN`
4. Ne yaptığını kısaca yaz
5. Diğer ekip üyeleri review eder → **Merge**

Alternatif terminal:
```bash
gh pr create --base main --head member/demir --title "Demir: WAF güncellemesi" --body "Ne değişti açıklaması"
```

---

## Hangi Dosyada Kim Çalışır?

| Kişi | Branch | Konu | Dosyalar |
|------|--------|------|----------|
| Ozan | `member/ozan` | SQL Injection + arama modülü | `app.py` → `_search_products()` |
| Demir | `member/demir` | WAF tespit motoru | `security/waf.py` |
| Arda | `member/arda` | Auth + loglama | `security/auth.py`, `database.py` |

Herkes kendi dosyalarında çalışır, başkasının dosyasına dokunmadan önce ekip grubunda yaz.

---

## Çakışma Olursa

```bash
git checkout member/SENIN-ISMIN
git pull origin main          # main'deki son değişiklikleri al
# Çakışan dosyaları düzenle
git add .
git commit -m "Merge main into member/SENIN-ISMIN"
git push
```

---

## Branch İsimlendirme Kuralları

- Küçük harf: `member/ozan`, `member/demir`, `member/arda`
- Feature branch: `feature/rapor-taslagi`, `feature/slide-deck` gibi de açılabilir
