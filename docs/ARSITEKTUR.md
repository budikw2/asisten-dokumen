# Arsitektur Repo dan Data

## Dua jenis repo
| Repo | Isi | Visibilitas |
|---|---|---|
| **asisten-dokumen** (ini) | Aturan umum, formulir kosong, skrip rakit, skenario uji | Privat milik pengelola, atau publik bila aman |
| **data-firma-[kode]** (satu per firma) | Berkas Firma (BF), Berkas Format (BT), File 02 terisi, folder proyek | **Selalu privat** |

Jangan menaruh banyak firma dalam satu repo. Satu kesalahan izin akan membuka data semua firma.

## Yang tidak boleh masuk repo mana pun
NIK, rekening, kata sandi, harga penawaran sebelum dibuka, dokumen rahasia klien. `build.py --check` memindai pola NIK, NPWP, dan kata sandi, tetapi itu hanya jaring pengaman, bukan jaminan.

## Alur perubahan
1. Buat cabang, ubah berkas di `core/` atau `template/`.
2. Naikkan `VERSION` dan tulis `CHANGELOG.md`.
3. Buka pull request. `CODEOWNERS` mewajibkan persetujuan admin.
4. Gabungkan ke `main`. CI menjalankan pemeriksaan.
5. Beri tag `vX.Y`. CI membuat rilis berisi file gabungan untuk diunduh.

## Memakai di AI
- Sekarang: unduh `ASISTEN_DOKUMEN_LENGKAP.txt` dari halaman Rilis, unggah ke chat atau Project (lihat docs/PROMPT_PEMBUKA.txt).
- Website nanti: server mengambil `core/` lewat GitHub API dengan token di sisi server sebagai pesan sistem. Berkas Firma milik firma yang login ditambahkan dari database atau repo privat firma.
- Kapsul Sesi proyek sebaiknya pindah ke database sungguhan, bukan GitHub.
