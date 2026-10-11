# Proyek UTS: Klasifikasi Land Use Land Cover (LULC) Jawa Timur (Sentinel-2A & SVM)

Repositori ini memuat implementasi lengkap proyek data science spasial untuk klasifikasi 6 kelas tutupan lahan di Provinsi Jawa Timur menggunakan citra satelit Sentinel-2A Level-2A (openEO CDSE) dan algoritma tunggal **Support Vector Machine (SVM)**.

---

## 1. Struktur Folder UTS

```text
UTS/
├── index.md                                      # Dokumen pengantar utama LULC
├── 01_business_understanding.ipynb               # Pemahaman masalah, tujuan bisnis & data science
├── 02_data_understanding.ipynb                   # Eksplorasi dataset piksel, profil spektral, korelasi
├── 03_data_preparation.ipynb                     # Centroid aggregation poligon & stratified split 80:20
├── 04_modeling_evaluasi_svm.ipynb                # Pelatihan Pipeline StandardScaler + SVM (SVC RBF) & evaluasi
├── 05_visualisasi_peta_folium.ipynb              # Rekonstruksi poligon spasial & peta aktual (ground truth)
├── 06_visualisasi_prediksi_model.ipynb           # Peta evaluasi spasial SVM (benar vs salah pada data uji)
├── 07_visualisasi_prediksi_raster_jatim.ipynb    # Klasifikasi regional skala raster Jawa Timur (~250 m)
├── 08_streamlit_app.ipynb                        # Modul pembuatan app.py & requirements.txt
├── 09_kesimpulan.ipynb                           # Sintesis temuan ilmiah & rekomendasi operasional
├── app.py                                        # Aplikasi Web Dashboard Interaktif Streamlit
├── requirements.txt                              # Dependensi Python untuk deployment
├── README.md                                     # Panduan lengkap proyek
├── data/                                         # Direktori berkas masukan (piksel_s2.csv, jatim_250m.tif)
└── output/                                       # Seluruh keluaran (CSV, PNG, HTML, GeoTIFF, Model .joblib)
```

---

## 2. 6 Kelas Tutupan Lahan (LULC) & Fitur Spektral

- **6 Kelas Target**:
  1. `Sawah` (`#FFD92F`)
  2. `Bangunan` (`#E41A1C`)
  3. `Hutan` (`#2E7D32`)
  4. `Danau` (`#4FC3F7`)
  5. `Laut` (`#0D47A1`)
  6. `Mangrove` (`#8E44AD`)
- **9 Fitur Spektral**:
  - 5 Band: `B02` (Blue), `B03` (Green), `B04` (Red), `B08` (NIR), `B11` (SWIR)
  - 4 Indeks: `NDVI`, `NDWI`, `MNDWI`, `NDBI`

---

## 3. Metodologi & Hasil Kinerja Model

- **Mitigasi Spatial Autocorrelation Leakage**:
  - Agregasi centroid pada level poligon (`poligon_id`) menghasilkan 357 poligon sampel unik.
  - Pembagian *Stratified Train-Test Split (80:20)* menghasilkan 285 poligon latih dan 72 poligon uji independen.
- **Model Machine Learning Tunggal**:
  - `Pipeline([('scaler', StandardScaler()), ('svm', SVC(kernel='rbf', C=10, gamma='scale', probability=True, random_state=42))])`
- **Hasil Pengujian Riil (Data Uji 72 Poligon)**:
  - **Akurasi**: `88.89%` (64 dari 72 poligon benar)
  - **Macro F1-Score**: `0.8879`
  - **Weighted F1-Score**: `0.8887`

---

## 4. Urutan Menjalankan Notebook (01 sampai 09)

Jalankan notebook secara berurutan agar jembatan data di folder `output/` terbentuk:
1. `01_business_understanding.ipynb`
2. `02_data_understanding.ipynb`
3. `03_data_preparation.ipynb` *(menghasilkan output/df_poligon_split.csv)*
4. `04_modeling_evaluasi_svm.ipynb` *(menghasilkan output/model_svm.joblib & output/df_poligon_pred_svm.csv)*
5. `05_visualisasi_peta_folium.ipynb` *(menghasilkan output/peta_aktual_lulc.html)*
6. `06_visualisasi_prediksi_model.ipynb` *(menghasilkan output/peta_prediksi_svm.html)*
7. `07_visualisasi_prediksi_raster_jatim.ipynb` *(menghasilkan output/prediksi_lulc_jatim_svm.tif & output/peta_prediksi_raster_jatim.html)*
8. `08_streamlit_app.ipynb` *(menghasilkan app.py & requirements.txt)*
9. `09_kesimpulan.ipynb` *(rekapitulasi capaian proyek)*

---

## 5. Cara Menjalankan Aplikasi Web Streamlit

Pastikan seluruh pustaka pada `requirements.txt` terpasang:
```bash
pip install -r requirements.txt
```

Jalankan aplikasi dari dalam folder `UTS`:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka pada peramban web di alamat `http://localhost:8501`.
