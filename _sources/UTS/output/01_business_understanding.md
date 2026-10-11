# Ringkasan Business Understanding: LULC Jawa Timur (Sentinel-2A & SVM)

## 1. Tujuan Bisnis
Menyediakan peta tematik klasifikasi Land Use Land Cover (LULC) Provinsi Jawa Timur 6 kelas yang akurat dan dapat diperbarui secara berkala untuk mendukung perencanaan tata ruang wilayah (RTRW), perlindungan lahan pertanian (LP2B), dan pemantauan kelestarian lingkungan pesisir serta hutan.

## 2. Tujuan Data Science
Membangun model klasifikasi 6 kelas (Sawah, Bangunan, Hutan, Danau, Laut, Mangrove) berbasis Support Vector Machine (SVC kernel RBF, C=10, gamma='scale') dengan fitur 5 band spektral (B02, B03, B04, B08, B11) dan 4 indeks spektral (NDVI, NDWI, MNDWI, NDBI). Evaluasi dilakukan pada tingkat agregasi poligon untuk mencegah kebocoran spasial.

## 3. Kriteria Keberhasilan
- Akurasi pengujian >= 85% dan Macro F1 >= 0.85 pada data uji independen.
- Tidak terjadi spatial data leakage (pembagian data berbasis poligon).
- Sistem visualisasi Web-GIS interaktif dan dashboard Streamlit berfungsi penuh tanpa galat.

## 4. Ruang Lingkup dan Batasan
- Wilayah studi: Provinsi Jawa Timur (termasuk Kepulauan Kangean).
- Citra satelit: Sentinel-2A Level-2A dari openEO CDSE (komposit Agustus 2024).
- Metode tunggal: Pipeline StandardScaler + SVM (SVC RBF).
- Resolusi data latih: 10-20 m (agregasi poligon ground truth); Resolusi raster regional: ~250 m.