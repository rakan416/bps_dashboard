# Sistem ETL & Otomasi Dashboard BPS Kabupaten Madiun

## Latar Belakang
Proyek ini dikembangkan untuk mendukung kegiatan monitoring lapangan di BPS Kabupaten Madiun. Sebelumnya, data monitoring tersebar di tiga file Excel yang berbeda (Alokasi, Landmark, dan Rekap LKM), sehingga menyulitkan proses pembaruan data ke dalam Dashboard Visualisasi.
Kode ini berfungsi sebagai middleware ETL (Extract, Transform, Load) yang secara otomatis menggabungkan ketiga sumber data tersebut menjadi satu kesatuan dataset yang bersih, lalu mengirimkannya ke Supabase untuk ditampilkan di [Looker Studio](https://lookerstudio.google.com/reporting/f1f72020-0d09-45f5-a058-557ca6c9a4f6).

## Fitur Utama
* **Automated Merging** -> Menggabungkan 3 file Excel dengan struktur berbeda berdasarkan kunci unik wilayah (`idsls`).
* **Data Cleaning** -> Menangani data kosong (*missing value*) dan kesalahan format secara otomatis.
* **Supabase Integration** -> Koneksi langsung ke database cloud yang terhubung dengan Looker Studio.

## 👥 Kredit dan Pengembang
Dibuat sebagai bagian dari kegiatan **Magang di BPS Kabupaten Madiun**
dan dibuat Oleh:
* Rakan Refaya Dewangga
* M. Raihan Firdaus
