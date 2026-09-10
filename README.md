### Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

    Ketika seorang pengguna mengetik alamat personal website saya http://localhost:8000/ lalu membuka bagian education, maka url nya akan ikut berubah menjadi http://localhost:8000/education/. Ketika pengguna menekan enter setelah mengetik tersebut, file pertama yang menghandle ini adalah portofolio/urls.py, file ini hanya membaca bagian depan saja dan kalau dia melihat ada lanjutan pada url seperti /education/ maka tugasnya dilanjutkan oleh main/urls.py untuk mencocokkan bagian mana yang sesuai dengan alamat.

    Setelah ditemukan bagian yang cocok dengan alamat maka tugas akan dilanjutkan oleh main/views.py. Fungsi show_education yang terletak dalam views.py berfungsi mengatur data apa yang ditampilkan dengan cara request data ke models.py agar mengambil data dari database db.sqlite3, data tersebut akan dikumpulkan sesuai field yang ada lalu dibungkus dalam sebuah variabel yaitu context. 

    Setelah data yang dibutuhkan sudah siap maka selanjutnya data tersebut akan masuk ke file education.html. Data yang diambil dari database akan ditampilkan melalui variabel penampung (contohnya {{ edu.institution }} dsb). Django akan otomatis menampilkan data sesuai variabel penampungnya yang sudah diatur dalam models.py dan , jika datanya masih kosong maka django akan menampilkan data yang berada di tag {% empty %} untuk menampilkan pesan alternatif. Setelah semua data berhasil ditempelkan ke dalam file HTML, Django akan mengeiim kembali hasilnya agar bisa dilihat oleh pengguna.

    Dalam pengerjaannya sendiri saya bayak memnggunakan bantuan Gemini untuk membantu saya memahami alur yang terjadi pada model MVT serta mengklarifikasi tiap langkah yang dijelaskan di tutorial agar saya lebih paham suatu langkah itu sebenarnya apa yang terjadi di balik layar, apa perannya dalam model MVT dan mengapa alur langkahnya harus begini.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

    Tujuan data disimpan dalam model adalah untuk memisahkan cara menyimpan dan menampilkan data. Template sendiri bertipe HTML yang berfungsi untuk mengatur struktur visual sedangkan models berfungsi untuk megatur struktur data pada database. Jika data ini langsung ditulis di HTML (Hardcoded) sebenarnya tidak masalah dalam skala kecil, namun saat proyek semakin besar ini menjadi tidak fleksibel karena tiap kali kita ingin membuat perubahan maka kita perlu mencari kode yang ingin kita ubah secara manual diantara ratusan baris, jika data ini terletak di beberapa halaman maka kita perlu mencari dan merubah data tersebut secara manual satu-per-satu. Hal ini juga membuat kode rawan rusak karena banyak perubahan yang dilakukan hanya untuk merubah satu data. Oleh karena itu maka kita sebaiknya menggunakan database agar lebih aman dan lebih fleklsibel untuk melakukan perubahan data dalam proyek.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

    Perintah makemigrations sendiri berfungsi untuk membaca serta memeriksa setiap perubahan yang ingin kita lakukan dalam models.py (contohnya menambah class baru atau field pada classs yang sudah ada). Django akan seecara otomatis membuat blueprint dari models.py yang baru dalam bentuk file yang akan disimpan di folder migrations.

    Jika kita jalankan perintah migrate maka python akan mengeksekusi perubahan yang kita tulis dengan cara memodifikasi database dalam db.sqlite3, ini adalah penyebabnya mengapa kita perlu menulis makemigrations dan migrate ketika melakukan perubahan dalam models.py karena perintah ini yang sebenarnya mengeksekusi perubahan dalam database. 

    Contoh perubahan model yang mengharuskan saya menjalankan kedua perintah ini adalah ketika saya pertama kali membuat class education, field yang tulis adalah nama institusi, posisi pendidikan, durasi, dan deskripsi. Tak lama setelah saya migrate, saya berpikir jika tampilannya akan lebih baik jika saya menambah logo institusi. Jadi saya kembali ke file models dan menambah field logo_url yang akan menjadi variabel penampung untuk menampilkan logo. Setelah saya tambahkan maka saya jalankan perintah makemigrations dan migrate agar perubahan ini terjadi di database. 



