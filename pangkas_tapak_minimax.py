"""pangkas_tapak_minimax.py — TokenLedger: tinggalkan model MiniMax sahaja.

Arahan BOZ 19 Nov 2026: "tinggal model minimax je, yang lain semua buang."

Disentuh: data.json (model, inventori, provider_kira, modal.model, connection_guna, baki,
ringkas), opencode_models.json (kosong + nota), model.json (mma sahaja).
Bahagian sejarah agregat (`hari`) dikekalkan — ia jumlah penggunaan, bukan senarai model.

Backup: *.bak-minimax-<masa>
"""
import json
import shutil
import time

CAP = time.strftime("%Y%m%d-%H%M%S")
NOTA = "Dipangkas 19 Nov 2026 (arahan BOZ): hanya model MiniMax dikekalkan; Mistral/OpenCode/Keyless dibuang."


def simpan(nama: str, data) -> None:
    shutil.copy2(nama, f"{nama}.bak-minimax-{CAP}")
    with open(nama, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def main() -> int:
    d = json.load(open("data.json", encoding="utf-8"))

    d["model"] = [m for m in (d.get("model") or []) if "MiniMax" in str(m.get("model", ""))]
    d["inventori"] = [m for m in (d.get("inventori") or [])
                      if str(m.get("provider")) == "mma" or str(m.get("penuh", "")).startswith("mma/")]
    d["provider_kira"] = {"mma": len(d["inventori"])}
    modal = d.get("modal") if isinstance(d.get("modal"), dict) else {}
    modal["model"] = [m for m in (modal.get("model") or [])
                      if "minimax" in str(m.get("penyedia", "")).lower()
                      or "minimax" in str(m.get("nama", "")).lower()]
    d["modal"] = modal
    asal_guna = len(d.get("connection_guna") or [])
    d["connection_guna"] = [c for c in (d.get("connection_guna") or [])
                            if str(c.get("nama", "")).startswith("MiniMax")
                            or any(x in str(c.get("nama", "")) for x in
                                   ("ayogiakbar", "gienetic", "euploading", "arcadehearth", "galrut"))]
    d["baki"] = {}
    r = d.setdefault("ringkas", {})
    r["model_diguna"] = len(d["model"])
    r["model_tersedia"] = len(d["inventori"])
    r["connection"] = len(d["connection_guna"])
    r["connection_sihat"] = len(d["connection_guna"])
    r["provider"] = 1
    r["mistral_akaun"] = 0
    r["mistral_sihat"] = 0
    r["nota_pangkas"] = NOTA
    d["nota"] = NOTA + " " + str(d.get("nota", ""))
    simpan("data.json", d)
    print(f"data.json: model {len(d['model'])}, inventori {len(d['inventori'])}, "
          f"connection_guna {asal_guna}->{len(d['connection_guna'])}, baki dikosongkan")

    oc = json.load(open("opencode_models.json", encoding="utf-8"))
    asal_oc = len(oc.get("model") or [])
    oc["model"] = []
    for k in ("jumlah_percuma", "jumlah_aktif", "jumlah_deprecated", "konteks_maks", "bilangan_1j"):
        oc["meta"][k] = 0
    oc["meta"]["nota_pangkas"] = NOTA
    simpan("opencode_models.json", oc)
    print(f"opencode_models.json: {asal_oc} -> 0 model (MiniMax sahaja)")

    mo = json.load(open("model.json", encoding="utf-8"))
    asal_mo = len(mo.get("hasil") or [])
    mo["hasil"] = [h for h in (mo.get("hasil") or [])
                   if "minimax" in str(h.get("model", "")).lower()]
    mo["bilangan"] = {"jumlah": len(mo["hasil"]), "lulus": len(mo["hasil"]), "gagal": 0}
    mo["keterangan"] = str(mo.get("keterangan", "")) + " " + NOTA
    simpan("model.json", mo)
    print(f"model.json: {asal_mo} -> {len(mo['hasil'])} model (MiniMax sahaja)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
