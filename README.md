# Asisten Dokumen (Edisi Pemula)

Pipeline prompt untuk membantu karyawan baru atau awam di firma kontraktor dan konsultan Indonesia menyusun dokumen kerja, dengan format yang selalu mengikuti ketentuan terbaru dari pusat atau klien.

## Isi
| Folder | Isi |
|---|---|
| `core/` | File 01 (inti), 03 (format dan template), 04 (buku gaya dan kamus), 05 (basis data sementara), 06 (profil model) |
| `template/` | File 02 (konfigurasi firma, formulir kosong) |
| `docs/` | Panduan admin, prompt pembuka, arsitektur repo |
| `tests/` | Skenario uji |
| `build/` | `build.py` untuk memeriksa dan merakit file gabungan |

## Memakai
```
python build/build.py --check   # periksa konsistensi dan data terlarang
python build/build.py           # hasilkan dist/ASISTEN_DOKUMEN_LENGKAP.txt dan .md
```
Atau unduh file gabungan dari halaman **Releases**. Panduan lengkap: `docs/00_PANDUAN_ADMIN.md`.

## Penting
- Repo ini **tidak boleh** berisi data firma. Berkas Firma dan Berkas Format disimpan di repo privat per firma (`docs/ARSITEKTUR.md`).
- Asisten tidak dapat memeriksa sendiri apakah format dari pusat sudah versi terbaru. Itu tugas admin dan pengguna.
- Isi regulasi, K3, pajak, dan kontrak harus dicek Legal, HSE, atau Keuangan.
