# Ekip Git Workflow

Bu repoda herkes kendi branch'inde çalışır, bitince `main`'e birleştiririz.

## Branch Yapısı

```
main                  ← Ana proje (hocaya sunulacak, stabil versiyon)
develop               ← Entegrasyon (opsiyonel, birleştirme test alanı)
member/ozan           ← Ozan'ın çalışma alanı
member/arkadas1       ← 1. arkadaşın çalışma alanı
member/arkadas2       ← 2. arkadaşın çalışma alanı
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

## Kendi Branch'ini Oluşturma

`SENIN-ISMIN` yerine kendi adını yaz (küçük harf, boşluksuz):

```bash
git checkout main
git pull origin main
git checkout -b member/SENIN-ISMIN
git push -u origin member/SENIN-ISMIN
```

Örnek:
```bash
git checkout -b member/ali
git push -u origin member/ali
```

---

## Günlük Çalışma

```bash
# Kendi branch'ine geç
git checkout member/SENIN-ISMIN

# Kod yaz, test et...

git add .
git commit -m "Ali: WAF pattern listesine yeni kural eklendi"
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
gh pr create --base main --head member/SENIN-ISMIN --title "Ali: WAF güncellemesi" --body "Ne değişti açıklaması"
```

---

## Hangi Dosyada Kim Çalışır?

| Kişi | Konu | Dosyalar |
|------|------|----------|
| Kişi 1 | SQL Injection + arama modülü | `app.py` → `_search_products()` |
| Kişi 2 | WAF tespit motoru | `security/waf.py` |
| Kişi 3 | Auth + loglama | `security/auth.py`, `database.py` |

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

- Küçük harf, tire ile: `member/ali`, `member-ayse` değil → `member/ayse`
- Türkçe karakter kullanma: `member/ozan` ✅ — `member/özan` ❌
- Feature branch: `feature/rapor-taslagi`, `feature/slide-deck` gibi de açılabilir
