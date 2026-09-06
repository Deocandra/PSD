# Memahami Angka-Angka di Balik Statistika Deskriptif

Sebelum data polutan diolah lebih jauh — baik untuk mencari pola, membuat prediksi, atau membangun model — kita perlu dulu "berkenalan" dengan data itu sendiri. Proses inilah yang disebut **Exploratory Data Analysis (EDA)**, dan salah satu alat bantunya adalah tabel ringkasan angka yang dikenal sebagai **statistika deskriptif**.

Tabel ini biasanya menyajikan sekumpulan angka untuk tiap variabel polutan (NO₂, CO, SO₂, O₃), dan masing-masing angka itu bercerita tentang sisi yang berbeda dari data. Berikut penjelasannya, dikelompokkan menjadi empat kategori besar.

## Kategori 1: Di Mana Pusat & Batas Datanya?

**Rata-rata (Mean)**

Ini adalah "titik tengah" data secara matematis — dihitung dengan menjumlahkan semua nilai lalu membaginya dengan berapa banyak data yang ada:

$$ \bar{x} = \frac{\sum_{i=1}^{n} x_i}{n} $$

Sederhananya: total semua kadar polutan, dibagi jumlah hari pengamatan yang datanya valid.

**Median**

Kalau Mean dihitung lewat penjumlahan, Median justru dicari lewat **pengurutan**. Susun semua data dari yang terkecil sampai terbesar, lalu lihat nilai yang berada tepat di tengah:
- Kalau jumlah datanya ganjil, Median = nilai pas di posisi tengah: $X_{(n+1)/2}$
- Kalau genap, Median = rata-rata dua nilai yang berada di tengah: $\frac{X_{n/2} + X_{(n/2)+1}}{2}$

Kelebihan Median dibanding Mean: ia **tidak mudah "terseret"** kalau ada satu-dua nilai ekstrem (outlier) dalam data. Makanya kalau data punya banyak outlier, Median sering jadi patokan yang lebih jujur dibanding Mean.

**Min & Max**

Ini yang paling sederhana — cukup urutkan data dari kecil ke besar, lalu ambil ujung-ujungnya:
- $Min$ = data paling awal ($X_1$)
- $Max$ = data paling akhir ($X_n$)

Gunanya untuk tahu seberapa lebar "rentang" nilai yang pernah tercatat.

**Overall Sum**

Ini murni penjumlahan seluruh nilai dalam satu kolom, tanpa dibagi apa pun:

$$ Sum = \sum_{i=1}^{n} x_i $$

## Kategori 2: Seberapa Menyebar Datanya?

**Standar Deviasi**

Bayangkan tiap titik data punya "jarak" ke nilai rata-rata. Standar deviasi mengukur, secara rata-rata, seberapa jauh jarak-jarak itu:

$$ s = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}} $$

- Standar deviasi **kecil** → data cenderung berkumpul rapat di sekitar rata-rata (stabil).
- Standar deviasi **besar** → data tersebar lebar, fluktuasinya tinggi.

**Varians**

Ini sebenarnya "saudara kembar" dari standar deviasi — bedanya cuma di akar kuadrat. Varians adalah standar deviasi **sebelum diakarkan**:

$$ s^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1} $$

Karena itu, kalau kamu sudah tahu nilai standar deviasi, tinggal dikuadratkan saja untuk dapat variansnya (atau sebaliknya, diakarkan).

## Kategori 3: Bagaimana Bentuk Sebaran Datanya?

**Skewness (Kemencengan)**

Metrik ini menjawab pertanyaan: "apakah data condong ke satu sisi?"

$$ Skewness = \frac{n}{(n-1)(n-2)} \sum_{i=1}^{n} \left(\frac{x_i - \bar{x}}{s}\right)^3 $$

Cara membacanya:
- **≈ 0** → sebaran data simetris, seperti kurva lonceng normal.
- **Positif** → "ekor" data memanjang ke kanan, artinya ada beberapa nilai yang jauh lebih tinggi dari mayoritas. Contohnya SO₂ dengan skewness 2.124 — menandakan ada lonjakan-lonjakan tinggi sesekali di tengah data yang umumnya rendah.
- **Negatif** → kebalikannya, ekor memanjang ke kiri.

**Kurtosis (Keruncingan)**

Kalau skewness bicara soal arah kemencengan, kurtosis bicara soal **seberapa ekstrem** nilai-nilai pencilan (outlier) yang muncul:

$$ Kurtosis = \left[ \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum \left(\frac{x_i - \bar{x}}{s}\right)^4 \right] - \frac{3(n-1)^2}{(n-2)(n-3)} $$

- **≈ 0 (Mesokurtik)** → distribusinya "normal", tidak terlalu runcing atau datar.
- **Positif (Leptokurtik)** → puncak data tajam, ekornya tebal — pertanda banyak outlier ekstrem. Contoh nyatanya SO₂ dengan kurtosis 19.221, angka yang sangat tinggi.
- **Negatif (Platikurtik)** → sebaran datanya lebih "rata"/datar dibanding distribusi normal. O₃ dengan nilai -0.375 termasuk kategori ini.

## Kategori 4: Seberapa "Bersih" Kualitas Datanya?

Kelompok metrik ini jadi penting banget khususnya untuk data yang diambil dari API atau citra satelit — karena proses perekamannya rawan gagal di tengah jalan.

- **No. missings** — menghitung berapa banyak sel yang kosong sama sekali (tidak terekam) di periode tertentu.
- **No. NaNs** — beda dengan missing murni, ini menghitung entri yang "ada" tapi nilainya tidak bisa didefinisikan secara matematis (misalnya hasil dari pembagian 0/0).
- **No. +infs / No. -infs** — menghitung kemunculan nilai "tak terhingga" (infinity), baik positif maupun negatif.

Cara menghitungnya sama semua: tinggal cari dan hitung (frekuensi) berapa baris yang mengandung kondisi-kondisi khusus tersebut.

---

# Implementasi Analisis Data Polutan: Dari Cloud Database ke KNIME

Panduan ini menguraikan tahapan-tahapan untuk menghubungkan database PostgreSQL di platform Aiven, melakukan inspeksi data menggunakan HeidiSQL, serta mengekstraksi metrik statistika deskriptif memanfaatkan KNIME Analytics Platform.

## Langkah 1: Memperoleh Kredensial Database dari Aiven

Sebelum menyambungkan koneksi melalui aplikasi apa pun, kita membutuhkan informasi kredensial server.
1. Akses *dashboard* atau console **Aiven**, lalu arahkan ke proyek yang dimiliki.
2. Buka tab **Overview** pada layanan (*service*) PostgreSQL yang sedang beroperasi (`pg-c4fbe52`).
3. Pada bagian **Connection information**, catat parameter-parameter berikut ini:
   * **Host:** `pg-1e75e6f1-psdp2.b.aivencloud.com`
   * **Port:** `12280`
   * **User:** `avnadmin`
   * **Password:** (Klik ikon mata atau opsi *copy* untuk menyalin kata sandi rahasia)
   * **SSL mode:** `require`
4. Pastikan Anda telah mengunduh sertifikat SSL (klik **Show** pada bagian *CA certificate* kemudian unduh) apabila *client* yang Anda gunakan mensyaratkannya.

![Aiven PostgreSQL Console](../../img/dbonline.png)

---
## Langkah 2: Mengonfigurasi Koneksi di dbeaver

dbeaver digunakan untuk meninjau tabel beserta datanya secara langsung sebelum diproses lebih lanjut.
1. Buka aplikasi **dbeaver**. Pada panel sebelah kiri (Browser), klik new data conection
2. Pilih jenis database yang akan digunakan, pilih PostgreSQL.
3. Pada ke tab **Connection**, terapkan konfigurasi di bawah ini:
   * **Host name/address:** Isikan informasi Host yang diperoleh dari langkah 1.
   * **Port:** Isikan `12280` (atau sesuai dengan *Port* pada langkah 1).
   * **Username:** Ketikkan `avnadmin`.
   * **Password:** Tempelkan (*paste*) kata sandi dari langkah 1, dan centang opsi **Save password?**.
4. Klik **Finish** guna menyimpan konfigurasi dan memulai koneksi.

![Konfigurasi Session Manager pgAdmin](../../img/dbkoneksi.png)

---

## Langkah 3: Melakukan Inspeksi Tabel Data di DBeaver

Setelah koneksi berhasil, kita perlu memverifikasi ketersediaan data mentah beserta kesesuaian formatnya.
1. Pada panel sebelah kiri DBeaver, navigasikan *tree* server yang baru dibuat menuju Databases > `polutan_ngawi` > Schemas > `public` > Tables > `polutan_ngawi`.
2. Klik dua kali (atau klik kanan lalu pilih **View/Edit Data**) pada tabel `polutan_ngawi` tersebut hingga terbuka tab **Data**.
3. Pastikan kolom data deret waktu (*time-series*) telah ditampilkan dengan tepat, yang meliputi kolom `date`, `NO2`, `SO2`, `O3`, dan `CO`.
4. Perlu diketahui bahwa pada tahapan ini merupakan hal yang lumrah bila dijumpai nilai `[NULL]` pada beberapa baris (contohnya kolom `NO2` dan `SO2` pada tanggal 2025-08-24, atau seluruh kolom polutan pada 2025-09-16). Nantinya, nilai tersebut akan teridentifikasi sebagai *missing values* pada saat tahap analisis.

![Tampilan Data Polutan di pgAdmin](../../img/dbtampilan.png)

---

## Langkah 4: Menyusun Alur Kerja (Workflow) di KNIME

Beralih menuju KNIME Analytics Platform guna menarik data dari database dan melakukan perhitungan statistiknya secara otomatis.
1. Jalankan **KNIME Analytics Platform** lalu buatlah *workflow* (alur kerja) yang baru.
2. Tarik (*drag-and-drop*) *node* di bawah ini dari *Node Repository* menuju ke *workspace*:
   * **PostgreSQL Connector:** Berfungsi menghubungkan KNIME dengan server Aiven.
   * **DB Table Selector:** Berfungsi untuk menyeleksi tabel di dalam database.
   * **DB Reader:** Berfungsi untuk memuat tabel ke dalam memori KNIME.
   * **Statistics:** Berfungsi untuk menghitung metrik-metrik statistik.
3. Hubungkan setiap *node* tersebut mengikuti urutan yang telah disebutkan di atas.
4. **Konfigurasi Node:**
   * Lakukan klik ganda pada **PostgreSQL Connector**, lalu isikan *Hostname*, *Port*, *Database name* (`Polutan_ngawi`), serta *Credentials* (User & Password) yang identik dengan langkah 1 dan 2.
   * Lakukan klik ganda pada **DB Table Selector**, kemudian pilih skema `public` serta tabel `polutan_ngawi`.
5. Klik kanan pada **DB Reader** lalu pilih opsi **Execute**. Jika prosesnya berhasil, lampu indikator di bagian bawah *node* akan berubah menjadi hijau.

![Alur Kerja Database dan Statistik di KNIME](../../img/knime01.png)

---

## Langkah 5: Membaca Output Statistika Deskriptif

Setelah data berhasil dimuat ke dalam KNIME, tahapan yang terakhir adalah menjalankan perhitungan analitiknya.
1. Klik kanan pada node **Statistics** kemudian pilih **Execute**.
2. Bila lampu indikator telah berwarna hijau, klik kanan kembali pada node **Statistics** lalu pilih menu **Statistics View** (atau ikon bergambar kaca pembesar).
3. Tabel metrik statistik akan ditampilkan, yang memuat:
   * **Min, Max, Mean:** Guna mengamati rentang serta nilai rata-rata dari masing-masing polutan.
   * **Std. deviation & Variance:** Guna meninjau tingkat fluktuasi nilai gas di udara.
   * **Skewness & Kurtosis:** Guna melihat bentuk asimetri dan tingkat keberadaan nilai-nilai yang ekstrem (*outlier*).
   * **No. missings:** Menyatakan jumlah data yang kosong (sebagai contoh, pada gas $CO$ terdapat 73 data yang kosong).
   * **Histogram:** Menyajikan visualisasi mengenai sebaran datanya.
![Tabel Hasil Output Node Statistics](../../img/knimeview01.png)

### Perhitungan Manual

Perhitungan manual di bawah ini menggunakan hasil ringkasan statistik yang sudah diperoleh dari tools (tabel: Min, Mean, Std. Dev, Skewness, Kurtosis, No. Missing), dengan jumlah baris valid dihitung sebagai $n = 366 - \text{No. Missing}$ (total 366 hari dikurangi jumlah data yang kosong).

---

## 1. NO₂

Diketahui: $\bar{x} = 2.43\text{E-}5$, $s = 6.91\text{E-}6$, No. Missing $= 66$, sehingga $n = 366 - 66 = 300$.

**a. Standar Deviasi & Variansi**

Standar Deviasi ($s$) sudah diketahui langsung dari tabel sebesar $6.91\text{E-}6$. Variansi diperoleh dengan mengkuadratkannya:

$$
v = s^2 = (6.91\text{E-}6)^2 = 4.7748\text{E-}11
$$

**b. Skewness**

$$
Skewness = \underbrace{\frac{n}{(n-1)(n-2)}}_{A} \underbrace{\sum_{i=1}^{n}\left(\frac{x_i-\bar{x}}{s}\right)^3}_{B}
$$

$$
A = \frac{300}{(300-1)(300-2)} = \frac{300}{89102} = 0.0033671
$$

$$
B = \frac{Skewness}{A} = \frac{0.3406}{0.0033671} \approx 101.155
$$

$$
Skewness = 0.0033671 \times 101.155 = 0.3406
$$

**c. Kurtosis**

$$
Kurtosis = \left[ \underbrace{\frac{n(n+1)}{(n-1)(n-2)(n-3)}}_{A} \underbrace{\sum \left(\frac{x_i - \bar{x}}{s}\right)^4}_{B} \right] - \underbrace{\frac{3(n-1)^2}{(n-2)(n-3)}}_{C}
$$

$$
C = \frac{3(300-1)^2}{(300-2)(300-3)} = \frac{268203}{88506} = 3.0303
$$

$$
A = \frac{300(301)}{(299)(298)(297)} = \frac{90300}{26463414} = 0.0034125
$$

$$
B = \frac{Kurtosis + C}{A} = \frac{1.0964 + 3.0303}{0.0034125} \approx 1209.14
$$

$$
Kurtosis = (0.0034125 \times 1209.14) - 3.0303 = 1.0964
$$

**d. Overall Sum**

$$
OS = \bar{x} \times n = 0.0000243 \times 300 = 0.00729
$$

---

## 2. SO₂

Diketahui: $\bar{x} = 3.77\text{E-}5$, $s = 0.0001$, No. Missing $= 41$, sehingga $n = 366 - 41 = 325$.

**a. Standar Deviasi & Variansi**

$$
v = s^2 = (0.0001)^2 = 1\text{E-}8
$$

**b. Skewness**

$$
A = \frac{325}{(324)(323)} = \frac{325}{104652} = 0.0031063
$$

$$
B = \frac{Skewness}{A} = \frac{-1.7454}{0.0031063} \approx -561.87
$$

$$
Skewness = 0.0031063 \times (-561.87) = -1.7454
$$

*Catatan: Skewness bernilai negatif pada SO₂ menandakan ekor distribusi memanjang ke kiri — berbeda dari ketiga polutan lain yang cenderung positif.*

**c. Kurtosis**

$$
C = \frac{3(324)^2}{(323)(322)} = \frac{314928}{104006} = 3.0280
$$

$$
A = \frac{325(326)}{(324)(323)(322)} = \frac{105950}{33707064} = 0.0031432
$$

$$
B = \frac{16.5301 + 3.0280}{0.0031432} \approx 622.24
$$

$$
Kurtosis = (0.0031432 \times 622.24) - 3.0280 = 16.5301
$$

*Catatan: Kurtosis SO₂ (16.5301) jauh lebih tinggi dibanding polutan lain — mengindikasikan sebaran data SO₂ Leptokurtik, banyak nilai ekstrem/outlier dibanding distribusi normal.*

**d. Overall Sum**

$$
OS = \bar{x} \times n = 0.0000377 \times 325 = 0.0122525
$$

---

## 3. O₃

Diketahui: $\bar{x} = 0.1156$, $s = 0.0023$, No. Missing $= 5$, sehingga $n = 366 - 5 = 361$.

**a. Standar Deviasi & Variansi**

$$
v = s^2 = (0.0023)^2 = 5.29\text{E-}6
$$

**b. Skewness**

$$
A = \frac{361}{(360)(359)} = \frac{361}{129240} = 0.0027932
$$

$$
B = \frac{0.429}{0.0027932} \approx 153.586
$$

$$
Skewness = 0.0027932 \times 153.586 = 0.429
$$

**c. Kurtosis**

$$
C = \frac{3(360)^2}{(359)(358)} = \frac{388800}{128522} = 3.0252
$$

$$
A = \frac{361(362)}{(360)(359)(358)} = \frac{130682}{46223280} = 0.0028268
$$

$$
B = \frac{0.0926 + 3.0252}{0.0028268} \approx 1102.86
$$

$$
Kurtosis = (0.0028268 \times 1102.86) - 3.0252 = 0.0926
$$

*Catatan: Kurtosis O₃ bernilai negatif (Platikurtik) — sebarannya lebih datar dibanding distribusi normal, sedikit outlier ekstrem.*

**d. Overall Sum**

$$
OS = \bar{x} \times n = 0.1156 \times 361 = 41.7316
$$

---

## 4. CO

Diketahui: $\bar{x} = 0.0288$, $s = 0.0031$, No. Missing $= 40$, sehingga $n = 366 - 40 = 326$.

**a. Standar Deviasi & Variansi**

$$
v = s^2 = (0.0031)^2 = 9.61\text{E-}6
$$

**b. Skewness**

$$
A = \frac{326}{(325)(324)} = \frac{326}{105300} = 0.0030959
$$

$$
B = \frac{0.2761}{0.0030959} \approx 89.192
$$

$$
Skewness = 0.0030959 \times 89.192 = 0.2761
$$

**c. Kurtosis**

$$
C = \frac{3(325)^2}{(324)(323)} = \frac{316875}{104652} = 3.02827
$$

$$
A = \frac{326(327)}{(325)(324)(323)} = \frac{106602}{34035900} = 0.0031326
$$

$$
B = \frac{0.1242 + 3.02827}{0.0031326} \approx 1006.28
$$

$$
Kurtosis = (0.0031326 \times 1006.28) - 3.02827 = 0.1242
$$

**d. Overall Sum**

$$
OS = \bar{x} \times n = 0.0288 \times 326 = 9.3888
$$

---

### Ringkasan Perbandingan Antar Polutan

| Polutan | n (valid) | Skewness | Kurtosis | Interpretasi Singkat |
|---|---|---|---|---|
| NO₂ | 300 | 0.3406 | 1.0964 | Sedikit condong kanan, sedikit lebih runcing dari normal |
| SO₂ | 325 | -1.7454 | 16.5301 | Condong kiri kuat, sangat runcing (banyak outlier ekstrem) |
| O₃ | 361 | 0.429 | 0.0926 | Condong kanan ringan, sebaran mendekati normal/agak datar |
| CO | 326 | 0.2761 | 0.1242 | Condong kanan ringan, mendekati distribusi normal |