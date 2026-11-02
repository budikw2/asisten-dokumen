# Desain web

Sumber desain tampilan web Asisten Dokumen (tanpa login). Format `.dc.html` adalah sumber artboard dari kanvas desain, `canvas.json` memuat posisi dan urutannya.

| Berkas | Halaman |
|---|---|
| `desain/Main.dc.html` | 1. Beranda |
| `desain/Kerja.dc.html` | 2. Ruang kerja (dengan banner kuota) |
| `desain/Firma.dc.html` | 3. Data firma |
| `desain/Format.dc.html` | 4. Format aktif |
| `desain/Ponsel.dc.html` | 5. Ruang kerja di ponsel |
| `desain/Batas.dc.html` | 6. Batas pemakaian habis |
| `desain/Sambung.dc.html` | 7. Sambungkan AI Anda (kunci API milik pengguna) |

Catatan rancangan:
- Tanpa login. Data firma dibawa lewat Berkas Firma, pekerjaan lewat Kapsul Sesi.
- Situs tidak menampilkan nama agen atau model yang dipakai. Nama penyedia hanya muncul sebagai pilihan pengguna di halaman 7.
- Kunci API milik pengguna dirancang hanya disimpan di peramban. Ini harus dipastikan saat implementasi.
