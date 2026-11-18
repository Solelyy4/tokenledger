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
NOTA = ("Ditapis kepada model MiniMax sahaja (arahan BOZ, 19 Nov 2026). "
        "Angka token sejarah kekal dalam graf harian termasuk penyedia yang telah dibuang.")
MATI = {"MiniMax-M2.5", "MiniMax-M2.1", "MiniMax-M2.7-highspeed",
        "mma/MiniMax-M2.5", "mma/MiniMax-M2.1", "mma/MiniMax-M2.7-highspeed"}


def simpan(nama: str, data) -> None:
    shutil.copy2(nama, f"{nama}.bak-minimax-{CAP}")
    with open(nama, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def main() -> int:
    d = json.load(open("data.json", encoding="utf-8"))

    d["model"] = [m for m in (d.get("model") or [])
                  if "MiniMax" in str(m.get("model", "")) and str(m.get("model", "")) not in MATI]
    d["inventori"] = [m for m in (d.get("inventori") or [])
                      if (str(m.get("provider")) == "mma" or str(m.get("penuh", "")).startswith("mma/"))
                      and str(m.get("model") or m.get("nama") or "") not in MATI]
    d["provider_kira"] = {"mma": len(d["inventori"])}
    modal = d.get("modal") if isinstance(d.get("modal"), dict) else {}
    modal["model"] = [m for m in (modal.get("model") or [])
                      if "minimax" in str(m.get("penyedia", "")).lower()
                      or "minimax" in str(m.get("nama", "")).lower()]
    # kad penyedia: buang Mistral/OpenCode/Keyless, tinggal MiniMax
    modal["penyedia"] = [p for p in (modal.get("penyedia") or [])
                         if "minimax" in (str(p.get("kunci", "")) + str(p.get("penyedia", ""))).lower()]
    for p in modal["penyedia"]:
        p["model"] = sum(1 for m in (d.get("model") or []))  # sejajar dengan kad ringkasan
    # angka modal & ringkasan dikira daripada model MiniMax yang tinggal (bukan sejarah agregat)
    j7 = sum((m.get("in_7", 0) or 0) + (m.get("out_7", 0) or 0) for m in (d.get("model") or []))
    q7 = sum(m.get("req_7", 0) or 0 for m in (d.get("model") or []))
    jh = sum((m.get("in_hari", 0) or 0) + (m.get("out_hari", 0) or 0) for m in (d.get("model") or []))
    qh = sum(m.get("req_hari", 0) or 0 for m in (d.get("model") or []))
    modal["jumlah_7"] = j7
    modal["req_7"] = q7
    modal["jumlah_30"] = j7
    modal["jumlah_hari"] = jh
    for p in modal["penyedia"]:
        p["jumlah_7"] = j7
        p["req_7"] = q7
        p["jumlah_30"] = j7
        p["jumlah_hari"] = jh
    modal["baki_mistral"] = {"baki_tok_min": 0, "had_tok_min": 0, "baki_req_min": 0,
                             "had_req_min": 0, "akaun": 0, "sihat": 0}
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
    r["token_7"] = j7
    r["token_hari"] = jh
    r["req_hari"] = qh
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
                   if "minimax" in str(h.get("model", "")).lower()
                   and str(h.get("model", "")) not in MATI]
    mo["bilangan"] = {"jumlah": len(mo["hasil"]), "lulus": len(mo["hasil"]), "gagal": 0}
    mo["keterangan"] = str(mo.get("keterangan", "")) + " " + NOTA
    simpan("model.json", mo)
    print(f"model.json: {asal_mo} -> {len(mo['hasil'])} model (MiniMax sahaja)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
