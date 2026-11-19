# SIMUTEH: Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra

**Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra (SIMUTEH)** adalah alat bantu berbasis pengolahan citra digital untuk membantu petugas sortir kelompok tani teh rakyat di Kabupaten Sukabumi dalam menggolongkan mutu daun teh secara obyektif berdasarkan estimasi persentase luas bercak cacar daun (*blister blight*)[cite: 2].

Dokumentasi ini menyajikan rangkuman pengembangan sistem dari **Evaluasi Pertemuan 1–4 (`v0.1`)** hingga **Praktikum Lanjutan Pertemuan 5–6 (`v0.2-tepi` dan `v0.3-morfologi`)** pada Mata Kuliah Computer Vision[cite: 2, 5].

---

## 👤 Identitas Pemilik
- **Nama:** Shinta Lavera
- **NIM:** 2330511008
- **Kelas:** 7A - Teknik Informatika
- **SEED Dataset:** 1008
- **Institusi:** Universitas Muhammadiyah Sukabumi (UMMI)
- **Repositori:** [github.com/shintaLavera/simuteh-2330511008](https://github.com/shintaLavera/simuteh-2330511008)

---

## 📂 Struktur Repositori
```text
simuteh-2330511008/
├── data/
│   └── sintetis/               # 60 citra sintetis (teh_001 s.d. teh_060) + mask acuan
├── hasil/                      # Keluaran evaluasi & parameter JSON
│   ├── b1_bgr_rgb.png
│   ├── b2_kb_kanal.csv
│   ├── b3_histogram_5kondisi.png
│   ├── b4_tabel_penapis.csv
│   ├── param_praproses.json    # Parameter praproses (P1-P4)
│   ├── param_bercak.json       # Parameter segmentasi & saring bercak (P5-P6)
│   ├── p5_tabel_tepi.csv       # Evaluasi Sobel, Prewitt, LoG, Canny
│   ├── p5_f1_kondisi.png       # Grafik F1 tepi per kondisi cahaya
│   ├── p6_eksperimen_se.csv    # Eksperimen ambang k dan structuring element
│   ├── p6_sebar_komponen.png   # Diagram sebar kebulatan vs rasio aspek
│   ├── p6_evaluasi_bercak.csv  # Evaluasi modul bercak.py pada 60 citra
│   └── p6_sebar_persen.png     # Diagram sebar persen bercak acuan vs prediksi
├── notebook/                   # Notebook eksperimen Google Colab
│   ├── B1_lingkungan.ipynb
│   ├── B2_citra_warna.ipynb
│   ├── B3_histogram.ipynb
│   ├── B4_penapisan.ipynb
│   ├── B5_praproses.ipynb
│   ├── P5_tepi.ipynb           # Bagian 1 & 2: Deteksi tepi & Canny (tag v0.2-tepi)
│   └── P6_morfologi.ipynb      # Bagian 3, 4, & 5: Morfologi & bercak.py (tag v0.3-morfologi)
├── src/                        # Modul Python reusable
│   ├── buat_dataset_sintetis.py
│   ├── praproses.py            # Modul praproses (P1-P4)
│   ├── utils_cv.py             # Utilitas pembacaan & tampilan citra
│   ├── utils_tepi.py           # Utilitas evaluasi tepi, IoU, dan mask awal (P5-P6)
│   └── bercak.py               # Modul analisis & klasifikasi mutu daun (P6)
├── requirements.txt            # Dependensi pustaka
└── README.md                   # Rangkuman laporan teknis
```[cite: 7, 10, 16, 22, 23]

---

## 📄 Ringkasan Pengembangan Sistem

### Tahap 1: Akuisisi & Praproses (`v0.1` — Pertemuan 1–4)[cite: 5]
- **Dataset Sintetis (SEED 1008):** 60 citra berukuran $640 \times 480$ piksel (20 sehat, 20 bercak ringan, 20 bercak berat) pada 5 kondisi pencahayaan (*normal, gelap, terang, kontras rendah, bayangan*).
- **Pemilihan Kanal:** **Kanal Red (R)** memberikan Kontras Bercak (KB) tertinggi ($4,14 \text{ s.d. } 10,64$ pada kelas berat) sekaligus menyamarkan tekstur tulang daun hijau[cite: 14].
- **Rangkaian Praproses:** *Resize* lebar $640\text{ px}$ $\rightarrow$ koreksi Gamma adaptif $\rightarrow$ CLAHE pada kanal **V** untuk cahaya tidak merata $\rightarrow$ **Penapis Median $3 \times 3$** untuk meredam derau tanpa mengikis bercak kecil[cite: 31, 32].

---

### Tahap 2: Deteksi Tepi (`v0.2-tepi` — Pertemuan 5)[cite: 2, 5]
- **Perbandingan Operator Tepi:** Pengujian **Sobel, Prewitt, Laplacian of Gaussian (LoG), dan Canny** terhadap tepi acuan daun dan bercak pada 40 citra berbercak membuktikan **Canny** pada **kanal R sesudah praproses** menghasilkan keseimbangan presisi dan *recall* (F1) tertinggi[cite: 8, 9, 10, 11].
- **Perbaikan Ambang Otomatis (`canny_persentil`):** Ambang otomatis berbasis median intensitas gagal pada citra kontras rendah karena mengukur tingkat kecerahan, bukan kekuatan gradien[cite: 12, 14]. Penggantian ambang atas menggunakan **persentil ke-$95$ / ke-$98$ magnitudo gradien Sobel** ($T_{\text{bawah}} = 0,4 \times T_{\text{atas}}$) berhasil memulihkan deteksi tepi pada seluruh kondisi cahaya[cite: 12, 14].
- **Keputusan Desain SIMUTEH:** Deteksi tepi **tidak dipakai** untuk mengisi area bercak karena hanya menghasilkan garis batas terbuka 1 piksel (luas bercak lebih cepat dan akurat dihitung dari mask biner morfologi), namun ekstraksi kontur dipakai untuk menghitung fitur bentuk pada tahap pengukuran[cite: 13, 14].

---

### Tahap 3: Operasi Morfologi & Analisis Komponen Terhubung (`v0.3-morfologi` — Pertemuan 6)[cite: 2, 5]
- **Pembersihan Citra Biner (`bersihkan`):** Citra biner awal dari ambang `median + 4.0 × MAD` pada kanal R dibersihkan menggunakan operasi **Opening** diikuti **Closing** dengan *structuring element* **Elips $5 \times 5$** untuk membuang bintik derau dan tepi daun tipis sekaligus menutup celah internal bercak[cite: 7, 16, 22].
- **Pelabelan & Penyaringan Bentuk (`ukur_dan_saring`):** Setiap komponen terhubung (konektivitas 8) diukur luasnya dalam piksel dan $\text{mm}^2$ ($1\text{ px} = 0,4375\text{ mm}$ pada jarak $200\text{ mm}$), lalu disaring dengan kriteria[cite: 5, 19, 20, 22]:
  - `luas_min >= 20` piksel[cite: 20, 22]
  - `kebulatan >= 0.5`[cite: 20, 22]
  - `rasio_aspek <= 1.8` (mengeliminasi sisa potongan tulang daun memanjang)[cite: 20, 22]
- **Klasifikasi Mutu (`analisis_daun`):**
  1. **Sehat:** Persentase luas bercak $< 0,1\%$[cite: 22]
  2. **Bercak Ringan:** $0,1\% \le \text{Persentase bercak} < 2,0\%$[cite: 22]
  3. **Bercak Berat:** $\text{Persentase bercak} \ge 2,0\%$[cite: 22]

---

## ⚙️ Konfigurasi Parameter JSON

### 1. `hasil/param_praproses.json` (P1–P4)
```json
{
  "lebar": 640,
  "gamma": 1.0,
  "clahe_clip": 2.0,
  "clahe_tile": 8,
  "penapis": "median",
  "kernel": 3,
  "sigma": 1.0,
  "tajam_k": 0.0
}
