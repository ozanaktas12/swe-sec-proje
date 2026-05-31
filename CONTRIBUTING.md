# Git Workflow — Kısa Özet

Detaylı rehber: [EKIP_REHBERI.md](EKIP_REHBERI.md)

## Branch'ler

```
main           ← Ana proje (PR ile merge, doğrudan push yok)
member/ozan    ← Ozan
member/demir   ← Demir
member/arda    ← Arda
```

## Komut Özeti

```bash
# İlk kurulum (bir kez)
git clone https://github.com/ozanaktas12/swe-sec-proje.git
cd swe-sec-proje
git checkout member/SENIN-ISMIN
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Her oturum
git checkout member/SENIN-ISMIN
git pull origin main
python app.py
# ... kod yaz ...
git add . && git commit -m "Isim: aciklama" && git push

# Main'e birleştirme → GitHub'da Pull Request aç
```

## Dosya Sahipliği

| Kişi | Dosya |
|------|-------|
| Ozan | `app.py` |
| Demir | `security/waf.py` |
| Arda | `security/auth.py`, `database.py` |
