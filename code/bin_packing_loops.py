#!/usr/bin/env python3
"""
simple_bin_packing.py

Versi sederhana untuk Studi Kasus 6:
- Baseline: First-Fit (FF)
- Optimized: First-Fit Decreasing (FFD)

Output:
- Penempatan per loop (bin)
- Jumlah loop
- Lower bound = ceil(sum(durations)/capacity)
- Waktu eksekusi tiap algoritma
- Opsional: simpan hasil ke folder results/

Cara pakai:
  python simple_bin_packing.py path/to/file.csv --col duration --capacity 60 --unit s --save

Jika kolom tidak diberikan, program mencoba gunakan kolom bernama 'duration' atau kolom numerik pertama.
Durasi dinormalisasi ke detik:
  unit='s' (detik), 'ms' (millisecond), 'min' (menit)
"""

import csv
import os
import sys
import time
import math
import argparse

# ------------------ fungsi pembacaan sederhana ------------------
def load_durations(csv_path, col=None, unit='s'):
    """
    Baca CSV, ambil kolom durasi, kembalikan list durasi (float detik).
    Jika kolom None, coba 'duration' atau kolom numerik pertama.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File tidak ditemukan: {csv_path}")

    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for r in reader:
            rows.append(r)

    if len(rows) == 0:
        raise ValueError("CSV tidak punya baris data.")

    # tentukan kolom durasi
    if col is None:
        # cari header 'duration' (case-insensitive)
        hdr_map = {h.lower(): h for h in headers}
        if 'duration' in hdr_map:
            col = hdr_map['duration']
        else:
            # pilih kolom numerik pertama
            chosen = None
            for h in headers:
                v = rows[0].get(h, '').strip()
                try:
                    float(v.replace(',',''))
                    chosen = h
                    break
                except:
                    continue
            col = chosen if chosen is not None else headers[0]

    durations = []
    for r in rows:
        raw = r.get(col, "")
        s = str(raw).strip().replace('"','').replace(',','')
        # coba float
        try:
            val = float(s)
        except:
            # coba format mm:ss atau mm:ss.xxx
            if ':' in s:
                parts = s.split(':')
                try:
                    if len(parts) == 2:
                        val = int(parts[0]) * 60 + float(parts[1])
                    elif len(parts) == 3:
                        val = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                    else:
                        val = 0.0
                except:
                    val = 0.0
            else:
                val = 0.0
        # normalisasi unit ke detik
        if unit == 'ms':
            val_sec = val / 1000.0
        elif unit == 'min':
            val_sec = val * 60.0
        else:
            val_sec = val
        durations.append(val_sec)
    return durations, col

# ------------------ First-Fit ------------------
def first_fit(durations, capacity):
    """Simple First-Fit: masukkan item ke bin pertama yang muat (urutan input)."""
    bins = []        # list of lists (item indices)
    loads = []       # sum per bin
    for i, w in enumerate(durations):
        placed = False
        for b in range(len(bins)):
            if loads[b] + w <= capacity + 1e-9:
                bins[b].append(i)
                loads[b] += w
                placed = True
                break
        if not placed:
            bins.append([i])
            loads.append(w)
    return bins, loads

# ------------------ First-Fit Decreasing ------------------
def first_fit_decreasing(durations, capacity):
    """Sort descending lalu jalankan First-Fit."""
    indexed = list(enumerate(durations))
    indexed.sort(key=lambda x: -x[1])  # largest first
    bins = []
    loads = []
    for idx, w in indexed:
        placed = False
        for b in range(len(bins)):
            if loads[b] + w <= capacity + 1e-9:
                bins[b].append(idx)
                loads[b] += w
                placed = True
                break
        if not placed:
            bins.append([idx])
            loads.append(w)
    return bins, loads

# ------------------ util & output ------------------
def lower_bound(durations, capacity):
    return math.ceil(sum(durations) / capacity)

def pretty_print(bins, loads, durations, title, capacity):
    print(f"\n--- {title} ---")
    print(f"Jumlah loop: {len(bins)} (kapasitas tiap loop = {capacity} detik)")
    for i, b in enumerate(bins, start=1):
        items = ", ".join(f"{idx}({durations[idx]:.2f}s)" for idx in b)
        print(f" Loop {i:02d}: load = {loads[i-1]:.2f}s | items = {len(b)} | {items}")
    print(f"Total durasi semua item: {sum(durations):.2f}s")
    print(f"Lower bound (ceil sum/capacity): {lower_bound(durations, capacity)}")

def save_bins_csv(bins, loads, durations, fname):
    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", fname)
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["bin_id", "item_index", "duration_s"])
        for b_idx, bin_items in enumerate(bins, start=1):
            for idx in bin_items:
                writer.writerow([b_idx, idx, f"{durations[idx]:.6f}"])
    return path

# ------------------ Main CLI ------------------
def main():
    parser = argparse = None
    try:
        import argparse
        parser = argparse.ArgumentParser(description="Simple First-Fit vs FFD for loop packing")
        parser.add_argument("csv", nargs='?', default="studikasus6/data/high_popularity_spotify_data_sample20.csv",
                    help="Path ke file CSV (default: studikasus6/data/high_popularity_spotify_data_sample20.csv)")
        parser.add_argument("--col", default=None, help="Nama kolom durasi (opsional)")
        parser.add_argument("--capacity", type=float, default=60.0, help="Kapasitas loop dalam detik (default 60)")
        parser.add_argument("--unit", choices=['s','ms','min'], default='s', help="Unit pada file: s|ms|min (default s)")
        parser.add_argument("--save", action="store_true", help="Simpan hasil ke folder results/")
        args = parser.parse_args()
    except Exception:
        # fallback simple prompt jika argparse tidak tersedia (jarang terjadi)
        if len(sys.argv) >= 2:
            csv_path = sys.argv[1]
            col = sys.argv[2] if len(sys.argv) >= 3 else None
            cap = 60.0
            unit = 's'
            save = False
        else:
            print("Usage: python simple_bin_packing.py path/to/file.csv --col duration --capacity 60 --unit s --save")
            return
    csv_path = args.csv
    col = args.col
    cap = args.capacity
    unit = args.unit
    save_flag = args.save

    print("Membaca file:", csv_path)
    durations, used_col = load_durations(csv_path, col=col, unit=unit)
    print(f"Kolom durasi yang dipakai: {used_col} (dinormalisasi ke detik). Jumlah item: {len(durations)}")
    print(f"Lower bound (ceil sum/capacity) = {lower_bound(durations, cap)}")

    # First-Fit
    t0 = time.perf_counter()
    ff_bins, ff_loads = first_fit(durations, cap)
    t1 = time.perf_counter()
    ff_time = t1 - t0

    # FFD
    t0 = time.perf_counter()
    ffd_bins, ffd_loads = first_fit_decreasing(durations, cap)
    t1 = time.perf_counter()
    ffd_time = t1 - t0

    # ringkasan
    print("\nRingkasan:")
    print(f" First-Fit  : bins = {len(ff_bins)}, time = {ff_time:.6f}s")
    print(f" First-FitD : bins = {len(ffd_bins)}, time = {ffd_time:.6f}s")
    pretty_print(ff_bins, ff_loads, durations, "Hasil First-Fit (urutan input)", cap)
    pretty_print(ffd_bins, ffd_loads, durations, "Hasil First-Fit Decreasing (urut turun)", cap)

    if save_flag:
        p1 = save_bins_csv(ff_bins, ff_loads, durations, "ff_bins.csv")
        p2 = save_bins_csv(ffd_bins, ffd_loads, durations, "ffd_bins.csv")
        with open(os.path.join("results","summary.txt"), "w", encoding='utf-8') as f:
            f.write(f"File: {csv_path}\nCapacity: {cap} s\n")
            f.write(f"Lower bound: {lower_bound(durations, cap)}\n")
            f.write(f"First-Fit: bins={len(ff_bins)}, time={ff_time:.6f}s\n")
            f.write(f"FFD: bins={len(ffd_bins)}, time={ffd_time:.6f}s\n")
        print(f"\nHasil disimpan: {p1}, {p2}, results/summary.txt")

    # catatan analisis singkat
    print("\nCatatan analisis:")
    print(" - Problem: bin packing (NP-hard).")
    print(" - Batas aproksimasi: FFD terikat teoretis <= (11/9)*OPT + 1.")
    print(" - Kompleksitas praktis: FF cepat O(n * bins) (bisa O(n^2) worst-case);")
    print("   FFD memerlukan sorting O(n log n) + assignment O(n * bins).")
    print("\nReferensi singkat tercantum di bagian bawah kode ini.")

if __name__ == "__main__":
    main()
