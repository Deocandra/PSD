# Ringkasan Inspeksi jawatimur.geojson

## Informasi File
- **Ukuran file**: 36,162 bytes (35.3 KB)
- **Jumlah titik koordinat asli**: 1,576
- **Jumlah titik setelah simplifikasi (0.001°)**: 1,553

## CRS dan Geometri
- **CRS**: EPSG:4326
- **Jenis geometri**: MultiPolygon
- **Jumlah fitur (baris)**: 1 (satu fitur level provinsi)
- **Kolom atribut**: ['nama']
- **Nilai atribut nama**: Jawa Timur
- **Jumlah bagian MultiPolygon**: 33 (pulau-pulau)

## Validitas Geometri
- **Geometri tidak valid**: 0 (0 = semua valid)
- **Tindakan**: tidak ada perbaikan diperlukan

## Bounding Box
| | Lama (hardcode) | GeoJSON Aktual |
|---|---|---|
| West | 110.89 | 110.8987 |
| South | -8.84 | -8.7804 |
| East | 115.45 | 116.2702 |
| North | -6.65 | -5.0530 |

**Keterangan**: Bbox lama (east=115.45) lebih kecil dari batas aktual (east=116.2702),
sehingga tidak mencakup Kepulauan Kangean. Bbox lama juga menyertakan koordinat Bali
(sekitar 115.0–115.7°BT, 8.0–8.9°LS) karena kotak persegi tidak mengikuti batas administrasi.

## Kepulauan Jawa Timur yang Tercakup
- ✅ Jawa Timur daratan utama
- ✅ Madura (bagian dari Part 0 atau Part 7)
- ✅ Kepulauan Kangean (Parts 11-29, east hingga 116.27°BT)
- ✅ Pulau Bawean (Part 9, sekitar 112.6°BT, 5.7°LS)
- ✅ Kepulauan Masalembu/Sumenep (Parts 30-32, north hingga -5.05°LS)
- ✅ Pulau Sapudi dan Raas (Parts 1-2)

## Daratan atau Perairan?
File ini mencakup **hanya batas daratan** dan kepulauan Jawa Timur.
Tidak mencakup perairan laut terbuka.
Konsekuensi: kelas Laut akan sangat berkurang atau hilang pada peta raster
karena piksel laut berada di luar batas – ini **perilaku yang diharapkan**, bukan kesalahan model.

## Luas Wilayah
- **Luas total batas administrasi**: 47,954.98 km² (proyeksi UTM Zone 49S/EPSG:32749)
- **Referensi resmi Jawa Timur**: ~47,922 km² (daratan)

## Pemeriksaan Sampel vs Batas
Lihat output/02_sampel_vs_batas.csv untuk tabel lengkap per kelas.
Lihat output/02_sampel_vs_batas_peta.png untuk visualisasi.
