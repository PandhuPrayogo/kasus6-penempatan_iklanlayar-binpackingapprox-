# Bin Packing Problem - Optimasi Loop Iklan

## Deskripsi Proyek

Implementasi algoritma bin packing untuk memasukkan durasi iklan (d₁, d₂, …, dₙ) ke dalam loop dengan kapasitas tetap C (misalnya 60 detik), dengan tujuan meminimalkan jumlah loop yang diperlukan.

**Dua metode yang dibandingkan:**

1. **Baseline** — First-Fit (FF): Masukkan setiap item dari urutan input ke bin pertama yang masih muat
2. **Optimized** — First-Fit Decreasing (FFD): Urutkan durasi dari terbesar ke terkecil, kemudian jalankan First-Fit

## Struktur Direktori
```
projek_kemas_loop/
├── simple_bin_packing.py        # Program utama
├── data/
│   └── your_ads_durations.csv   # Dataset durasi iklan (input)
├── results/                     # Folder hasil (jika menggunakan --save)
├── README.md
└── requirements.txt
```

## Instalasi dan Setup

### Prasyarat
- Python 3.x

### Install Dependensi
```bash
pip install -r requirements.txt
```

### Persiapan Dataset

Simpan file CSV berisi durasi iklan di folder `data/`.

**Kolom yang didukung:**
- `duration`, `duration_s`, `duration_ms`, atau nama kolom custom lainnya
- Durasi dapat dalam satuan detik (s), milidetik (ms), atau menit (min)

## Format CSV

### Contoh Format
```csv
duration_ms
15000
30000
10000
25000
20000
```

Atau:
```csv
duration_s,ad_name
15,Ad_A
30,Ad_B
10,Ad_C
25,Ad_D
```

## Cara Menjalankan

### Sintaks Dasar
```bash
python simple_bin_packing.py path/to/file.csv [OPTIONS]
```

### Opsi Parameter

| Parameter | Deskripsi | Default |
|-----------|-----------|---------|
| `--col` | Nama kolom durasi | Auto-detect |
| `--capacity` | Kapasitas loop (dalam detik atau sesuai unit) | 60 |
| `--unit` | Unit durasi (`s`, `ms`, `min`) | `s` |
| `--save` | Simpan hasil ke folder `results/` | False |

### Contoh Penggunaan

**Contoh 1: Durasi dalam milidetik**
```bash
python simple_bin_packing.py data/ads_durations.csv --col duration_ms --capacity 60000 --unit ms --save
```

**Contoh 2: Durasi dalam detik (default)**
```bash
python simple_bin_packing.py data/ads_durations.csv --capacity 60 --save
```

**Contoh 3: Auto-detect kolom**
```bash
python simple_bin_packing.py data/ads_durations.csv
```

## Output yang Dihasilkan

### Terminal

1. **Penempatan First-Fit (FF)**
   - Daftar loop dengan item dan durasi di setiap loop
   - Total jumlah loop yang digunakan

2. **Penempatan First-Fit Decreasing (FFD)**
   - Daftar loop dengan item dan durasi di setiap loop (setelah sorting)
   - Total jumlah loop yang digunakan

3. **Analisis Perbandingan**
   - Lower bound teoretis: ⌈∑dᵢ/C⌉ (jumlah minimum loop ideal)
   - Waktu eksekusi masing-masing algoritma
   - Perbandingan efisiensi kedua metode

### File Output (jika `--save` digunakan)

- `results/ff_bins.csv` — Hasil penempatan First-Fit
- `results/ffd_bins.csv` — Hasil penempatan First-Fit Decreasing
- `results/summary.csv` — Ringkasan perbandingan

## Ringkasan Algoritma

### 1. First-Fit (FF)

**Cara kerja:**
1. Untuk setiap item, cari bin pertama yang masih memiliki kapasitas cukup
2. Jika tidak ada bin yang cocok, buat bin baru
3. Masukkan item ke bin tersebut

**Karakteristik:**
- Sangat cepat dan sederhana
- Tidak ada jaminan optimal
- Kompleksitas: O(n · bins) → O(n²) worst case

**Kapan digunakan:**
- Memproses data secara real-time/streaming
- Dataset sangat besar dan butuh kecepatan
- Tidak memerlukan hasil optimal

### 2. First-Fit Decreasing (FFD)

**Cara kerja:**
1. Urutkan item berdasarkan durasi (terbesar ke terkecil)
2. Jalankan algoritma First-Fit pada urutan yang sudah disortir

**Karakteristik:**
- Lebih baik daripada FF dalam mayoritas kasus
- Jaminan aproksimasi: **FFD ≤ 11/9 · OPT + 1**
- Kompleksitas: O(n log n + n · bins)

**Kapan digunakan:**
- Memerlukan hasil mendekati optimal
- Data dapat diproses dalam batch
- Bersedia membayar biaya sorting untuk efisiensi lebih baik

## Analisis Teoretis

### Kompleksitas Masalah
- **Bin Packing Problem** adalah **NP-hard**
- Tidak ada algoritma polynomial yang menjamin solusi optimal untuk kasus umum

### Lower Bound Teoretis

$$\text{Lower Bound} = \left\lceil \frac{\sum_{i=1}^{n} d_i}{C} \right\rceil$$

- Jumlah minimum loop yang secara teoretis diperlukan
- Tidak selalu dapat dicapai dalam praktik
- Berguna sebagai benchmark untuk mengukur kualitas solusi

### Batas Aproksimasi FFD

**Teorema (Johnson, 1973):**

$$\text{FFD}(I) \leq \frac{11}{9} \cdot \text{OPT}(I) + 1$$

Artinya: FFD menggunakan **maksimal 22% lebih banyak** bin daripada solusi optimal (dalam kasus terburuk).

### Perbandingan Kompleksitas

| Algoritma | Kompleksitas | Jaminan Aproksimasi |
|-----------|--------------|---------------------|
| First-Fit (FF) | O(n²) worst case | Tidak ada |
| First-Fit Decreasing (FFD) | O(n log n) | ≤ 11/9 · OPT + 1 |
| Optimal (ILP) | Exponential | Optimal |

## Interpretasi Hasil

### Jika FFD << FF
FFD berhasil mengoptimalkan penempatan dengan signifikan → Dataset cocok untuk sorting heuristik

### Jika FFD ≈ FF
Dataset mungkin sudah cukup acak atau ukuran item relatif seragam

### Jika Hasil >> Lower Bound
- Dataset memiliki item dengan ukuran yang sulit di-pack efisien
- Pertimbangkan algoritma yang lebih canggih (Best-Fit, Branch and Bound)

## Contoh Kasus

### Input
```csv
duration_s
45
30
25
20
15
10
```

**Kapasitas loop:** 60 detik

### Hasil First-Fit (FF)
- Loop 1: [45, 10] → 55s
- Loop 2: [30, 25] → 55s
- Loop 3: [20, 15] → 35s
- **Total: 3 loop**

### Hasil First-Fit Decreasing (FFD)
- Loop 1: [45, 15] → 60s (optimal!)
- Loop 2: [30, 25] → 55s
- Loop 3: [20, 10] → 30s
- **Total: 3 loop**

**Lower Bound:** ⌈145/60⌉ = 3 loop

Dalam kasus ini, FFD mencapai solusi optimal!

## Catatan Debugging

### Kolom Tidak Terdeteksi
Gunakan parameter `--col` untuk menentukan nama kolom secara eksplisit:
```bash
python simple_bin_packing.py data.csv --col my_duration_column
```

### Unit Tidak Sesuai
Pastikan parameter `--unit` dan `--capacity` menggunakan satuan yang konsisten:
- Jika durasi dalam ms, gunakan `--unit ms --capacity 60000`
- Jika durasi dalam detik, gunakan `--unit s --capacity 60`

### Hasil Tidak Optimal
Jika FFD menghasilkan banyak bin kosong/kurang terisi:
- Periksa apakah ada item yang mendekati kapasitas C
- Pertimbangkan menyesuaikan kapasitas loop
- Coba algoritma Best-Fit atau Worst-Fit untuk perbandingan

## Pernyataan Keaslian (Untuk Laporan UTS)

> **Pernyataan Keaslian**
> 
> Kami menyatakan bahwa kode dan laporan ini adalah hasil kerja kelompok kami. Ide algoritma yang digunakan adalah materi umum yang dipelajari (First-Fit, First-Fit Decreasing untuk Bin Packing Problem); implementasi, eksperimen, dan analisis dilakukan oleh anggota tim: [Nama1, Nama2, Nama3]. Jika ada penggunaan sumber eksternal (paper, blog, AI), kami mencantumkan referensi dan menjelaskan bagian yang diadaptasi.

**Jika menggunakan bantuan AI:**
> Bagian kode X dihasilkan atau dibantu oleh AI (ChatGPT) dan telah saya modifikasi, verifikasi, dan pahami sepenuhnya.

## Referensi

Wajib dicantumkan dalam bibliografi laporan UTS:

1. Johnson, D. S. (1973). *Near-optimal bin packing algorithms*. Doctoral dissertation, Massachusetts Institute of Technology.

2. Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.

3. Wikipedia — Bin packing problem. https://en.wikipedia.org/wiki/Bin_packing_problem

4. Wikipedia — First-fit-decreasing bin packing. https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing

5. Coffman, E. G., Garey, M. R., & Johnson, D. S. (1996). Approximation algorithms for bin packing: A survey. In *Approximation algorithms for NP-hard problems* (pp. 46-93).

6. Delorme, M., Iori, M., & Martello, S. (2016). Bin packing and cutting stock problems: Mathematical models and exact algorithms. *European Journal of Operational Research*, 255(1), 1-20.

---

**Catatan:** Pastikan semua referensi di atas dicantumkan dalam laporan UTS Anda, tidak hanya di README.

## Lisensi

Proyek ini dibuat untuk keperluan akademik (UTS). Penggunaan di luar konteks akademik harus seizin pembuat.
