# Quasar Pulse — papan token & kuota bot Quasar

Laman awam: **https://solelyy4.github.io/quasar-pulse/**

Papan satu halaman yang memaparkan token sebenar, kuota yang dilaporkan penyedia, dan
kesihatan connection untuk bot Quasar (9router).

## Dua mod data

| Mod | Bila | Sumber |
|---|---|---|
| **LANGSUNG** | Dibuka di laptop BOZ (pelayan tempatan hidup) | `http://127.0.0.1:8890/api/data` |
| **SNAPSHOT** | Dibuka dari mana-mana peranti lain | `data.json` dalam repo ini |

Halaman cuba mod langsung dahulu (had 2.5s), kemudian jatuh ke snapshot. Lencana di
penjuru atas menunjukkan mod yang sedang aktif dan berapa lama data snapshot itu dikemas.

## Cara data dikemas kini

Snapshot dijana dan ditolak (push) oleh laptop setiap 15 minit:

```
python buat_snapshot.py      # di C:/Users/zahin/projects/papan-quasar
git commit -am "data: snapshot" && git push
```

Tugasan berjadual Windows: `QuasarPulse-Push` (setiap 15 min).

## Nota privasi

Snapshot diterbitkan **selepas** data peribadi di-mask:
- emel akaun MiniMax → `boza***@euploading.com`
- kunci Mistral hanya ditunjuk sebagai `kunci 01 · …FjQU` (4 aksara akhir)
- tiada kunci API, tiada token sesi, tiada laluan fail peribadi

## Bina semula

Fail `index.html` dijana dan disunting di `C:/Users/zahin/projects/papan-quasar/index.html`,
kemudian disalin ke sini. Animasi: SVG + CSS sahaja — tiada aset luar, tiada CDN.
