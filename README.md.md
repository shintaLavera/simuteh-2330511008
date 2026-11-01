# SIMUTEH: Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra

**Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra (SIMUTEH)** adalah alat bantu berbasis pengolahan citra digital untuk membantu petugas sortir kelompok tani teh rakyat di Kabupaten Sukabumi dalam menggolongkan mutu daun teh secara obyektif berdasarkan estimasi persentase luas bercak cacar daun (*blister blight*).

Dokumentasi ini menyajikan rangkuman dan garis besar dari **Laporan Evaluasi Praktikum Pertemuan 1–4** Mata Kuliah Computer Vision.

---

## 👤 Identitas Pemilik
* **Nama:** Shinta Lavera
* **NIM:** 2330511008
* **Kelas:** 7A - Teknik Informatika
* **SEED Dataset:** 1008
* **Institusi:** Universitas Muhammadiyah Sukabumi (UMMI)
* **Repositori:** [github.com/shintaLavera/simuteh-2330511008](https://github.com/shintaLavera/simuteh-2330511008)

---

## 📂 Struktur Repositori
```text
simuteh-2330511008/
├── data/
│   └── sintetis/         # 60 citra sintetis (teh_001 s.d. teh_060)
├── hasil/                # Hasil keluaran evaluasi & parameter
│   ├── b1_bgr_rgb.png
│   ├── b2_kb_kanal.csv
│   ├── b3_histogram_5kondisi.png
│   ├── b4_tabel_penapis.csv
│   └── param_praproses.json
├── notebook/             # Notebook eksperimen Google Colab
│   ├── B1_lingkungan.ipynb
│   ├── B2_citra_warna.ipynb
│   ├── B3_histogram.ipynb
│   ├── B4_penapisan.ipynb
│   └── B5_praproses.ipynb
├── src/                  # Modul Python pendukung
│   ├── buat_dataset_sintetis.py
│   ├── praproses.py
│   └── utils_cv.py
├── requirements.txt      # Dependensi pustaka
└── README.md             # Rangkuman laporan teknis
```

---

## 📄 Ringkasan Garis Besar Laporan (Overview)

### 1. Pendahuluan & Formulasi Masalah
* **Latar Belakang:** Pemilahan manual bercak cacar daun (*blister blight*) sering dipengaruhi oleh persepsi individual dan variasi cahaya tempat sortir.
* **Tujuan SIMUTEH:** Mengklasifikasikan daun ke dalam tiga kategori:
  1. **Sehat** (Bercak < 0,2%)
  2. **Bercak Ringan** (0,2% ≤ Bercak < 3,0%)
  3. **Bercak Berat** (Bercak ≥ 3,0%)
* **Pipeline 6 Tahap:** Akuisisi Citra $\rightarrow$ Praproses $\rightarrow$ Segmentasi Bercak $\rightarrow$ Ekstraksi Fitur $\rightarrow$ Klasifikasi $\rightarrow$ Interpretasi/Keputusan.
* **Semantic Gap & Etika:** Menjembatani perbedaan representasi angka piksel BGR/RGB dengan makna biologis daun. Risiko dikendalikan melalui penghapusan lokasi GPS/EXIF dan menjaga keputusan akhir tetap pada petugas.

### 2. Data & Rencana Akuisisi Citra
* **Dataset Sintetis (SEED 1008):** 60 citra berukuran $640 \times 480$ piksel, terbagi atas 20 sehat, 20 bercak ringan, dan 20 bercak berat di bawah 5 kondisi pencahayaan (normal, gelap, terang, kontras rendah, bayangan).
* **Aturan Akuisisi Kunci:**
  * Jarak kamera $\pm 20 \text{ cm}$ (maksimal $22,9 \text{ cm}$) tegak lurus nampan agar bercak $5 \text{ mm}$ tetap terdeteksi ($\ge 10 \text{ piksel}$).
  * Resolusi HP penuh, lalu di-resize ke lebar $640 \text{ piksel}$.
  * Foto menggunakan nampan polos dan alas acuan skala penggaris $5 \text{ cm}$.

### 3. Evaluasi Eksperimen & Perhitungan Manual

#### A. Pembentukan Citra & Ruang Warna
* **Kanal Warna Terbaik:** Keterpisahan bercak diukur menggunakan **Kontras Bercak (KB)**:
  $$\text{KB} = \frac{|\text{rerata bercak} - \text{rerata daun}|}{\text{simpangan baku daun}}$$
* **Temuan:** **Kanal Red (R)** menghasilkan nilai KB tertinggi secara konsisten di berbagai kondisi pencahayaan (KB $4,14 \text{ s.d. } 10,64$ pada kelas berat) karena penyerapan warna hijau daun dan pemantulan warna oranye bercak secara ekstrem.

#### B. Histogram & Perbaikan Citra Adaptif
* **Diagnosis Pencahayaan:** Ditentukan dari rerata, simpangan baku, % piksel gelap ($<30$), dan % piksel terang ($>205$).
* **Strategi Perbaikan:**
  * *Gelap:* Koreksi Gamma $\gamma = 0,5$.
  * *Terang:* Koreksi Gamma $\gamma = 1,8$.
  * *Kontras Rendah:* Peregangan kontras persentil 2–98.
  * *Bayangan:* **CLAHE** ($\text{clipLimit}=2,0$, $\text{gridSize}=8\times8$) pada kanal **V (Value)** untuk mencegah pergeseran nilai *Hue*.

#### C. Konvolusi & Penapisan Spasial
* **Penanganan Derau:** Pengujian peredaman derau Gaussian dan *salt-and-pepper*.
* **Hasil:** **Penapis Median $3 \times 3$** terpilih sebagai peredam derau paling optimal (PSNR $47,18 \text{ dB}$ pada derau $4\%$) tanpa mengikis atau menghilangkan area bercak kecil (berbeda dengan median $9\times9$ atau $15\times15$ yang merusak batas tepi).

#### D. Integrasi Praproses & Akurasi Rangkaian
* **Kendala Versi 1:** Struktur tulang daun terdeteksi sebagai bercak, menyebabkan akurasi awal hanya **38,3%**.
* **Solusi Revisi:** Penambahan operasi **morfologi opening** (elemen struktur elips $9 \times 9$) berhasil mengeliminasi tulang daun dan menaikkan akurasi klasifikasi status pada 60 citra hingga **86,7%**.

---

## 📊 Rangkaian Parameter Akhir (`param_praproses.json`)

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
```

---

## ⚡ Cara Menggunakan & Menjalankan Proyek

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/shintaLavera/simuteh-2330511008.git
   cd simuteh-2330511008
   ```

2. **Instalasi Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generasi Dataset Sintetis (Opsional):**
   ```bash
   python src/buat_dataset_sintetis.py
   ```

4. **Jalankan Evaluasi:**
   Buka file Jupyter Notebook di direktori `notebook/` menggunakan Google Colab atau Jupyter Lab untuk memverifikasi tahapan evaluasi B1 hingga B5.