"""pangkas_tapak.py — buang model mati dari TokenLedger (repo tapak web).

Bukti penyingkiran (diukur 19 Nov 2026, WIB):
  MiniMax-M2.5 / M2.1 / M2.7-highspeed  -> pool :8899 hang, tiada teks
  mistral/mistral-large-latest          -> 403
  oc/muse-spark-1.2 / oc/jev-1.13       -> 400 server_error
  opencode/* bertanda "deprecated"      -> 41 model dilapuk oleh penyedia

Fail disentuh: opencode_models.json, data.json, model.json
Backup: *.bak-pangkas-<masa>
"""
import json
import shutil
import time

MATI_MODEL = {"MiniMax-M2.5", "MiniMax-M2.1", "MiniMax-M2.7-highspeed"}
MATI_PENUH = {"mistral/mistral-large-latest", "oc/muse-spark-1.2-contributor-free",
              "oc/jev-1.13-free", "mmf/mimo-auto", "oc/union-alpha",
              "oc/muse-spark-1.3-contributor-free",
              "kgw/nvidia/nemotron-3-super-120b-a12b:free",
              "kgw/kwaipilot/kat-coder-pro-v2.5:free",
              "kgw/kilo-auto/frontier", "kgw/kilo-auto/balanced",
              "mistral/mistral-medium-latest"}
CAP = time.strftime("%Y%m%d-%H%M%S")


def simpan(nama: str, data) -> None:
    shutil.copy2(nama, f"{nama}.bak-pangkas-{CAP}")
    with open(nama, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def main() -> int:
    # ---------- 1. katalog OpenCode ----------
    oc = json.load(open("opencode_models.json", encoding="utf-8"))
    asal_oc = len(oc["model"])
    oc["model"] = [m for m in oc["model"] if m.get("status") == "aktif"]
    konteks = [m.get("konteks") or 0 for m in oc["model"]]
    oc["meta"]["jumlah_percuma"] = len(oc["model"])
    oc["meta"]["jumlah_aktif"] = len(oc["model"])
    oc["meta"]["jumlah_deprecated"] = 0
    oc["meta"]["konteks_maks"] = max(konteks) if konteks else 0
    oc["meta"]["bilangan_1j"] = sum(1 for k in konteks if k >= 1000000)
    oc["meta"]["nota_pangkas"] = (f"{asal_oc - len(oc['model'])} model deprecated dibuang "
                                  f"19 Nov 2026 — tak boleh serve, tak boleh tambah token")
    simpan("opencode_models.json", oc)
    print(f"opencode_models.json: {asal_oc} -> {len(oc['model'])} model (aktif sahaja)")

    # ---------- 2. statistik penggunaan ----------
    d = json.load(open("data.json", encoding="utf-8"))
    asal_d = len(d.get("model") or [])
    d["model"] = [m for m in (d.get("model") or [])
                  if m.get("model") not in MATI_MODEL and m.get("model") not in MATI_PENUH]
    d.setdefault("ringkas", {})["model_diguna"] = len(d["model"])
    d["ringkas"]["nota_pangkas"] = "model mati (M2.x, mistral-large, oc/*) dibuang 19 Nov 2026"
    simpan("data.json", d)
    print(f"data.json: {asal_d} -> {len(d['model'])} baris model digunakan")

    # ---------- 3. keputusan ujian model ----------
    mo = json.load(open("model.json", encoding="utf-8"))
    asal_mo = len(mo.get("hasil") or [])
    mo["hasil"] = [h for h in (mo.get("hasil") or []) if h.get("lulus")]
    mo["bilangan"] = {"jumlah": len(mo["hasil"]),
                      "lulus": len(mo["hasil"]), "gagal": 0}
    mo["keterangan"] = (mo.get("keterangan", "") +
                        " Dipangkas 19 Nov 2026: model gagal dibuang (tak boleh serve, "
                        "tak boleh tambah token).")
    simpan("model.json", mo)
    print(f"model.json: {asal_mo} -> {len(mo['hasil'])} model lulus (gagal dibuang)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
