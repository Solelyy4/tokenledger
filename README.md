# TokenLedger — akaun token model

Laman awam: **https://solelyy4.github.io/tokenledger/**

Papan satu halaman yang memaparkan jumlah token **setiap model**, baki kuota yang benar-benar
dilaporkan penyedia, dan sama ada token boleh ditambah — dibaca terus daripada rekod permintaan
9router (SQLite `usageHistory`).

## Isi papan

| Seksyen | Kandungan |
|---|---|
| Ringkasan | Jumlah token 7 hari, hari ini, 30 hari, model digunakan, akaun sihat |
| Token ikut model | Token masuk/keluar + jumlah setiap model, bahagian %, boleh susun & cari |
| Baki & modal | Angka yang dilaporkan sahaja: kadar Mistral (token/minit), mata kolam MiniMax |
| Boleh tambah? | Jawapan ikut penyedia — kuota terikat pada akaun, bukan pada model |
| Kesihatan sambungan | Akaun sihat vs bermasalah + ralat terkini |
| Model tersedia | Jumlah model & penyedia yang boleh dipanggil |

## Dua mod data

| Mod | Bila | Sumber |
|---|---|---|
| **LANGSUNG** | Dibuka di laptop BOZ (pelayan tempatan hidup) | `http://127.0.0.1:8890/api/data` |
| **SNAPSHOT** | Dibuka dari mana-mana peranti lain | `data.json` dalam repo ini |

Halaman cuba mod langsung dahulu, kemudian jatuh ke snapshot. Lencana di penjuru atas
menunjukkan mod aktif dan masa snapshot dikemas.

## Cara data dikemas kini

Snapshot dijana dan ditolak (push) oleh laptop setiap 15 minit:

```
python buat_snapshot.py      # di C:/Users/zahin/projects/papan-quasar
git commit -am "data: snapshot" && git push
```

Tugasan berjadual Windows: `QuasarPulse-Push` (setiap 15 min) — menjalankan
`papan-quasar/tolak_snapshot.py`, yang menulis ke folder ini.

Blok `modal` dalam `data.json` dijana oleh `papan-quasar/modal.py`:
token setiap model (1/7/30 hari) + klasifikasi kuota per penyedia.

## Nota kejujuran

Penyedia (Mistral, MiniMax) **tidak** menyediakan endpoint baki token per model. Yang ada hanya
had kadar seminit (Mistral) dan mata kolam (MiniMax). Papan menulis "tidak dilaporkan" dan tidak
mengarang angka baki.

## Nota privasi

Snapshot diterbitkan **selepas** data peribadi di-mask:
- emel akaun MiniMax → `boza***@euploading.com`
- kunci Mistral hanya ditunjuk sebagai `kunci 01 · …FjQU` (4 aksara akhir)
- tiada kunci API, tiada token sesi, tiada laluan fail peribadi

## Bina semula

Sumber halaman: `C:/Users/zahin/projects/papan-quasar/index.html` (disalin ke sini setiap push).
Tiada aset luar, tiada CDN, tiada animasi — SVG + CSS sahaja.
