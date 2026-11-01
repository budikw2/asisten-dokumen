#!/usr/bin/env python3
"""Merakit file gabungan Asisten Dokumen dari core/ dan template/.

Pemakaian:
  python build/build.py            # periksa lalu tulis dist/
  python build/build.py --check    # hanya periksa (untuk CI), tanpa menulis
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ORDER = [  # (nomor, folder, nama file)
    ("01", "core", "01_PIPELINE_INTI.txt"),
    ("02", "template", "02_KONFIGURASI_FIRMA.txt"),
    ("03", "core", "03_FORMAT_DAN_TEMPLATE.txt"),
    ("04", "core", "04_BUKU_GAYA_DAN_KAMUS.txt"),
    ("05", "core", "05_BASIS_DATA_SEMENTARA.txt"),
    ("06", "core", "06_PROFIL_MODEL.txt"),
]
HEAD = """# ASISTEN DOKUMEN v{v} (EDISI PEMULA): FILE GABUNGAN

Ini gabungan File 01 sampai 06 dalam satu berkas. Isinya sama dengan enam file terpisah.

## Petunjuk untuk Asisten (jangan ditampilkan ke pengguna)
- Berkas ini terdiri dari enam bagian besar. Tiap bagian diawali judul `# ... (FILE nn)` dan diakhiri `# [END OF FILE nn]`. Perlakukan masing-masing sebagai file tersendiri, dengan File 01 sebagai instruksi kerjamu.
- Bila pengguna mengunggah berkas ini, mulai dari File 01 Bagian 0 (Aktivasi). Pastikan keenam bagian terbaca penuh. Bila ada yang terpotong, katakan terus terang dan minta pengguna mengunggah ulang.
- File 02 di sini adalah formulir kosong. Status firma ditentukan menurut File 05 Bagian 2. Profil model dipilih menurut File 06.

---

"""
errors = []

def err(msg):
    errors.append(msg)

def main(check_only):
    texts = {}
    for nn, folder, name in ORDER:
        p = ROOT / folder / name
        if not p.exists():
            err(f"File hilang: {folder}/{name}")
            continue
        t = p.read_text(encoding="utf-8").strip()
        texts[nn] = t
        if not t.endswith("]"):
            err(f"{name}: tidak diakhiri penanda [END OF FILE]")
        if f"[END OF FILE {nn}]" not in t[-40:]:
            err(f"{name}: penanda akhir bukan [END OF FILE {nn}]")
    if errors:
        return finish()

    # 1. Versi konsisten
    if f"PIPELINE INTI v{VERSION}" not in texts["01"]:
        err(f"File 01: judul tidak memuat v{VERSION}")
    if f"Pipeline: {VERSION}" not in texts["05"]:
        err(f"File 05: 'Pipeline: {VERSION}' tidak ditemukan")
    if f"{VERSION} Edisi Pemula" not in texts["01"]:
        err(f"File 01: baris VERSI tidak memuat {VERSION}")

    # 2. Perintah di File 05 dan 06 harus ada di tabel perintah File 01
    for cmd in ["SETUPFIRMA", "CEKFIRMA", "EKSPOR FIRMA", "EKSPOR FORMAT", "IMPOR",
                "UBAHFIRMA", "/menu", "TIER RINGAN", "TIER STANDAR", "TIER TINGGI"]:
        if cmd not in texts["01"]:
            err(f"Perintah '{cmd}' tidak ada di File 01")

    # 3. Rujukan Bagian ke File lain harus ada
    for m in re.finditer(r"File 0([1-6]) Bagian (\d+)", "\n".join(texts.values())):
        f, b = m.group(1), m.group(2)
        body = texts["0" + f]
        if not re.search(rf"^#+\s*{b}\.", body, re.M) and not re.search(rf"^#+\s*[A-Z]?{b}\b", body, re.M):
            # Rujukan 'Bagian N' hanya diperiksa untuk file bernomor bagian angka
            if f in ("01", "05", "06"):
                err(f"Rujukan 'File 0{f} Bagian {b}' tidak punya judul bagian")
    # 4. Pindai pola data MERAH
    patterns = {
        "NIK (16 digit)": r"(?<!\d)\d{16}(?!\d)",
        "NPWP": r"\b\d{2}\.\d{3}\.\d{3}\.\d-\d{3}\.\d{3}\b",
        "kata sandi": r"(?i)\b(password|kata sandi)\s*[:=]\s*\S+",
    }
    for path in list((ROOT / "core").glob("*")) + list((ROOT / "template").glob("*")):
        t = path.read_text(encoding="utf-8", errors="ignore")
        for label, pat in patterns.items():
            if re.search(pat, t):
                err(f"{path.relative_to(ROOT)}: terdeteksi pola {label}")
    # 5. Berkas data firma tidak boleh ada di repo inti
    for pat in ("BF_*.txt", "BT_*.txt", "KAPSUL*"):
        for hit in ROOT.rglob(pat):
            if ".git" not in hit.parts:
                err(f"Berkas data firma tidak boleh di repo ini: {hit.relative_to(ROOT)}")
    if errors:
        return finish()

    body = HEAD.format(v=VERSION) + "\n\n---\n\n".join(texts[n] for n, _, _ in ORDER) + "\n"
    if not check_only:
        dist = ROOT / "dist"
        dist.mkdir(exist_ok=True)
        for ext in ("txt", "md"):
            (dist / f"ASISTEN_DOKUMEN_LENGKAP.{ext}").write_text(body, encoding="utf-8")
        print(f"OK: dist/ASISTEN_DOKUMEN_LENGKAP.txt dan .md ({len(body)} karakter)")
    else:
        print(f"OK: pemeriksaan lulus ({len(body)} karakter bila dirakit)")
    return finish()

def finish():
    if errors:
        print("GAGAL:")
        for e in errors:
            print(" -", e)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
