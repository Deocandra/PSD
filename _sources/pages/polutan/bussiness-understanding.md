# Business Understanding
## 1. Latar Belakang
Kondisi udara yang bersih menjadi salah satu penentu utama kesejahteraan masyarakat dan keberlanjutan ekosistem suatu wilayah. Bertambahnya jumlah kendaraan bermotor, berkembangnya kawasan industri, serta meningkatnya aktivitas pembangunan turut mendorong naiknya risiko pencemaran udara akibat gas-gas berbahaya. Kabupaten Ngawi, yang terletak di sisi barat Provinsi Jawa Timur dan terus mengalami pertumbuhan infrastruktur, juga berpotensi mengalami perubahan komposisi udara dari waktu ke waktu.

Empat parameter gas yang menjadi perhatian utama dalam pemantauan kualitas udara secara global antara lain:

- **Nitrogen Dioksida (NO₂):** umumnya berasal dari knalpot kendaraan bermotor dan proses produksi di sektor industri.
- **Karbon Monoksida (CO):** senyawa berbahaya yang muncul akibat proses pembakaran bahan bakar yang kurang sempurna.
- **Sulfur Dioksida (SO₂):** biasanya bersumber dari letusan gunung berapi maupun pembakaran bahan bakar fosil bersulfur tinggi.
- **Ozon (O₃):** terbentuk melalui reaksi kimia di atmosfer antara oksida nitrogen (NOx) dan senyawa organik volatil (VOC) yang dipicu oleh paparan sinar matahari.

Untuk memahami dinamika pencemaran udara di suatu daerah, diperlukan pengamatan yang dilakukan secara rutin dan berkesinambungan. Proyek ini menggunakan citra satelit Sentinel-5P yang diakses melalui platform Copernicus Data Space Ecosystem guna merekam konsentrasi keempat polutan tersebut di atas wilayah Kabupaten Ngawi dalam bentuk data deret waktu (Time Series), terhitung sejak Agustus 2025 hingga Agustus 2026.

## 2. Rumusan Masalah
Beberapa pertanyaan pokok yang hendak dijawab melalui eksplorasi data ini meliputi:
- Bagaimana pola perubahan konsentrasi harian gas polutan (NO₂, CO, SO₂, dan O₃) di wilayah Kabupaten Ngawi?
- Adakah indikasi pola musiman, kecenderungan naik dalam jangka panjang, ataupun kenaikan tidak wajar (anomali) pada kadar polusi udara di kawasan tersebut?

## 3. Tujuan Proyek
Eksplorasi data sains ini bertujuan untuk:
- Membangun proses otomatis pengambilan data satelit berbasis lokasi menjadi berkas tabular (CSV) yang siap diolah lebih lanjut.
- Menjalankan analisis data eksploratif (EDA) guna mengenali karakteristik dan kecenderungan perubahan konsentrasi gas polutan udara sepanjang waktu.
- Membentuk fondasi data historis yang memadai sebagai bekal untuk pemodelan prediktif (forecasting) kualitas udara pada periode berikutnya.

## 4. Manfaat Proyek
Diharapkan hasil pengolahan data ini dapat memberi manfaat bagi berbagai pihak, di antaranya:
- **Pemerintah / Pengambil Kebijakan:** menjadi bahan pertimbangan berbasis data dalam merumuskan kebijakan lingkungan, pengaturan arus lalu lintas, atau pengawasan sumber emisi.
- **Masyarakat Umum:** berperan sebagai sumber informasi yang jelas untuk menumbuhkan kepedulian warga terhadap perubahan kualitas udara harian di lingkungan tempat tinggalnya.
- **Peneliti / Praktisi Data:** memberikan contoh penerapan nyata (use case) pengolahan data spasial beresolusi tinggi ke dalam kerangka pemodelan deret waktu.
