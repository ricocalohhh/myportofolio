### Tugas 5

  1. Jelaskan apa itu *debouncing* dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

  * Debouncing adalah teknik optimasi pemrograman yang digunakan untuk menunda eksekusi suatu fungsi hingga beberapa saat setelah pengguna berhenti   melakukan suatu aksi.
  * Mengapa debouncing penting:
    - Tanpa debouncing, setiap ketikan karakter memicu satu HTTP Request. Mengetik kata dengan 10 karakter akan sangat mengganggu karena akan membuat 10 *request* beruntun. Dengan debouncing, *request* hanya dikirim satu kali setelah pengguna selesai mengetik.
    - Debouncing membantu menghindari kondisi di mana respons AJAX dari ketikan awal menimpa hasil pencarian ketikan akhir, sehingga UI tetap konsisten.
    - Debouncing juga menghemat bandwidth dan mengurangi pemrosesan data balasan JSON yang sudah tidak relevan (*stale requests*).
  

2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

* `fetch()` sendiri di JavaScript bersifat *asynchronous* dan mengembalikan sebuah objek `Promise`. Kata kunci `await` berfungsi untuk menunda eksekusi baris kode berikutnya sampai `Promise` tersebut selesai diproses dan mengembalikan objek `Response`.
* Fungsi utama await adalah menghentikan sementara eksekusi kode di dalam fungsi tersebut (baris selanjutnya) sampai proses request dari `fetch()` selesai dan mengembalikan data asli (Response).
* Yang akan terjadi jika Tidak Menggunakan `await`:
  - Variabel yang menampung hasil `fetch()` akan berisi objek `Promise <pending>`, bukan data HTTP Response.
  - Pemanggilan metode `.json()` akan menyebabkan *TypeError* (misal: `response.json is not a function`) karena `.json()` adalah metode milik `Response`, bukan `Promise`.
  - Alur eksekusi kode berjalan secara sinkron sebelum data selesai diunduh dari server, mengakibatkan kegagalan *rendering* DOM yang menyebabkan tampilan UI menjadi kosong/rusak.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

* Pengertian XSS:  
  *Cross-Site Scripting* atau XSS adalah kerentanan keamanan web di mana penyerang  berhasil menyisipkan skrip berbahaya (seperti `<script>...</script>` atau `<img src="x" onerror="...">`) ke dalam situs yang terpercaya. Skrip ini dieksekusi oleh browser pengguna lain yang ingin mengunjungi situs tersebut. Akibatnya penyerang dapat mencuri *session cookie*, token autentikasi, atau melakukan aksi ilegal.
* Mengapa Data AJAX/JavaScript Lebih Rentan:
  - Django Auto-Escaping: Engine Django Template secara otomatis menerapkan *context-aware HTML escaping* pada variabel `{{ variable }}` (mengubah `<` menjadi `&lt;`), sehingga browser hanya merendernya sebagai teks biasa.
  - Manipulasi DOM di JavaScript: Pengembang sering menggunakan `innerHTML` atau *template literals* (misalnya `` element.innerHTML = `<div>${item.title}</div>` ``). Jika `item.title` berisi skrip XSS, browser akan langsung menafsirkan dan mengeksekusinya sebagai HTML aktif.
  - Perlu Sanitasi Manual di Client-Side: Data JSON dari AJAX berbentuk *raw text*. Tanpa proteksi bawaan di tingkat JavaScript DOM, developer wajib menerapkan *defense-in-depth* berupa sanitasi di backend (`strip_tags`) dan *output escaping* di frontend (menggunakan `textContent` atau membuat elemen DOM secara eksplisit).

## AI Disclosure 

1. Tools AI yang Digunakan
* **Generative AI Tool:** Gemini AI
* **Penggunaan Utama:** Membantu penyusunan arsitektur AJAX (penanganan `Promise`/`await`), membantu implementasi sanitasi *Defense-in-Depth* terhadap serangan XSS, penanganan token CSRF pada *request* POST, serta memberi panduan dalam merancang fungsi *debouncing* pada pencarian *real-time*.

2. Strategi Prompting
* **Context-First Prompting:** Memberikan konteks lengkap file `views.py`, `forms.py`, dan skrip JavaScript di template HTML sebelum meminta perbaikan atau optimasi kode.
* **Constraint-Based Prompting:** Memberikan batasan aturan yang jelas, seperti "Tombol Edit dan Hapus cuma boleh muncul di card kalau user adalah Editor atau Superuser", serta "Tandai status error di JavaScript supaya pesan gagalnya muncul lewat Toast notification".
* **Verify before execute:** Meminta AI menjelaskan akar masalah error (misal penanganan HTTP Status 400 Bad Request pada validasi form) sebelum mengaplikasikan perubahan kode.

3. Analisis Kritis Keterbatasan AI & Perbaikan Manual
* **Penanganan Respons Error AJAX yang Terlalu Umum:** Kode awal dari AI menganggap semua error jaringan sama dan langsung menampilkan pesan error umum yang sama padahal alasan errornya berbeda
  **Perbaikan Manual:** Mengubah fungsi saveEducation di JavaScript untuk mengambil pesan ValidationError dari JSON respons HTTP status 400 (strip_tags) dan menampilkannya lewat Toast notification.
* **Kehilangan Field Durasi & Logo pada Payload JSON:** Serializer dasar buatan AI tidak menyertakan properti `duration` dan `logo_url` yang dibutuhkan oleh elemen renderer DOM JavaScript.  
  **Perbaikan Manual:** Memperbaiki fungsi `get_education_json` di `views.py` untuk memformat rentang tahun (`started_at` & `ended_at`) menjadi string `duration` serta menyertakan `logo_url` dalam respons JSON.
* **Penanganan Potensial XSS via `innerHTML`:** AI awal memberikan contoh manipulasi DOM menggunakan `innerHTML` yang rentan terhadap penyerangan XSS jika data mengandung tag HTML berbahaya.  
  **Perbaikan Manual:** Memperbarui fungsi pembangun card DOM JavaScript dengan menggunakan sanitasi `strip_tags` di `forms.py` (akan menghasilkan error 400 Bad Request jika disisipkan) serta mengganti penetapan teks menggunakan fungsi sanitasi HTML.

4. Log / Bukti Prompting
> *Daftar ringkasan prompt/interaksi utama dengan AI:*
> - **Pengguna:** *"Bagaimana cara mengimplementasikan fetch AJAX untuk membaca data JSON dari endpoint backend Django tanpa reload halaman?"*
> - **Pengguna:** *"Tolong audit kode Javascript DOM rendering ini, pastikan aman dari serangan XSS jika pengguna memasukkan tag <img src="x" onerror="...">."*
> - **Pengguna:** *"Kenapa saat pengujian XSS form mengembalikan response Bad Request 400? Apakah ini menandakan proteksi backend berjalan dengan benar?"*

### Tugas 6

1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!

* **Pengertian Representational State Transfer** 
  REST adalah gaya arsitektur untuk merancang komunikasi antara client dan server. Dalam REST, data dipandang sebagai *resource* yang memiliki alamat atau URL. Client dapat melakukan tindakan terhadap resource menggunakan metode HTTP, seperti GET, POST, PUT, PATCH, dan DELETE.
  - Contohnya, `/api/v1/experience/` digunakan untuk mengakses daftar pengalaman, sedangkan `/api/v1/experience/<uuid>/` digunakan untuk mengakses satu pengalaman tertentu.
* **Mengapa JSON saja belum cukup**
  - JSON hanya merupakan format pertukaran data. API yang mengembalikan JSON belum tentu mengikuti prinsip REST.
  - API REST juga perlu memiliki antarmuka yang konsisten, menggunakan URL untuk mengidentifikasi resource, dan menggunakan metode HTTP sesuai
    tindakan yang dilakukan.
  - Salah satu prinsip REST adalah *stateless*: 
    setiap request harus membawa informasi yang diperlukan untuk memprosesnya, tanpa bergantung pada konteks request sebelumnya yang disimpan server.
  - Pada proyek ini, autentikasi menggunakan `SessionAuthentication` Django, sehingga server menyimpan data sesi sedangkan pada implementasinya penggunaan sesi tidak sepenuhnya mengikuti prinsip stateless REST.
* **Perbedaan PUT dan PATCH:**
  - `PUT` digunakan untuk memperbarui resource secara menyeluruh. Client mengirimkan representasi lengkap sesuai field yang diwajibkan API.
    Contohnya, ketika seluruh data sebuah Experience diisi kembali dan dikirim ke `/api/v1/experience/<uuid>/`.
  - `PATCH` digunakan untuk memperbarui sebagian field. Contohnya, ketika Editor hanya ingin mengubah `title`, client cukup mengirimkan field
    `title` tanpa harus mengirim ulang deskripsi dan tanggal.
  - Pada API Experience, `partial=True` digunakan ketika metode request adalah `PATCH`, sehingga field yang tidak dikirim tetap menggunakan nilai
    sebelumnya.

2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?

* **Peran serializer**
  - Serializer mengubah objek Django, seperti objek `Experience`, menjadi representasi data Python yang dapat dirender menjadi JSON melalui proses
    *serialization*.
  - Serializer juga memeriksa dan mengubah data dari request menjadi data yang sudah divalidasi sebelum disimpan. Proses penerimaan dan pengolahan
    input ini disebut *deserialization*.
  - Pada proyek ini, `ExperienceSerializer` menentukan field yang ditampilkan, seperti `title`, `description`, `star_count`, dan `is_starred`.
* **Keuntungan dibandingkan dictionary manual**
  - Daftar field ditentukan secara eksplisit dalam satu class, sehingga bentuk respons lebih konsisten dan tidak perlu di render ulang pada tiap view.
  - Validasi dapat diletakkan dalam method seperti `validate_title` dan `validate_description`. Contohnya, tag HTML dibersihkan dengan `strip_tags` dan  
    judul kosong ditolak.
  - `ModelSerializer` dapat membaca definisi model dan menyediakan implementasi dasar untuk membuat serta memperbarui objek.
  - `SerializerMethodField` membantu menambahkan data hasil perhitungan yang bersifat *read-only*, seperti jumlah star dan status star pengguna.
  - Field akun sensitif, seperti email dan password hash, dapat tidak disertakan dalam daftar field respons.
* **Implementasi**
  `JsonResponse` dan dictionary manual sebenarnya tetap dapat digunakan, tetapi developer perlu menyusun representasi dan menangani validasi sendiri.
  Serializer membantu memusatkan aturan tersebut, terutama ketika API mendukung operasi baca dan tulis.

3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?

* **Autentikasi** adalah proses mengenali siapa yang mengirim request. Pada proyek ini, `SessionAuthentication` menggunakan sesi login Django untuk
  menentukan pengguna dan mengisi `request.user`.
  - Contohnya, setelah login sebagai Editor, request dapat dikenali sebagai request dari akun Editor tersebut.
  * **Otorisasi** adalah proses menentukan apakah pengguna tersebut boleh  melakukan tindakan tertentu. Pada DRF, pemeriksaan ini dapat dilakukan
  melalui *permission class*.
  - Contohnya, Endpoint star memakai `IsAuthenticated`, sehingga hanya pengguna yang sudah login yang dapat memberi atau membatalkan star.
* **Mengapa harus diperiksa di server**
  - Menyembunyikan tombol di template hanya mengubah tampilan. Pengguna masih dapat mengirim request langsung ke URL API menggunakan alat lain.
  - Permission class memeriksa setiap request yang masuk ke endpoint. Jika user tidak memiliki izin, server menolak tindakan tersebut dengan respons 403.
  - Dengan demikian, perlindungan data tetap berlaku meskipun tampilan dimodifikasi atau request dikirim tanpa melalui tombol di halaman.

4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?

* **Mengapa token CSRF diperlukan**
  - Ketika pengguna login, browser menyimpan cookie sesi dan dapat  mengirimkannya secara otomatis bersama request ke situs.
  - Dalam serangan *Cross-Site Request Forgery* (CSRF), situs lain dapat mencoba memanfaatkan sesi tersebut agar browser korban mengirim request
    yang tidak diinginkan.
  - Dengan `SessionAuthentication`, DRF memeriksa token CSRF untuk request  yang mengubah data dari pengguna yang terautentikasi, seperti POST,
    PUT, PATCH, dan DELETE.
  - Pada halaman Experience, token dibaca dari cookie dan dikirim melalui header `X-CSRFToken`. Server dapat menolak request jika token yang
    diperlukan tidak ada atau tidak valid.
* **Mengapa `force_authenticate` tidak cukup**
    `force_authenticate` memasang pengguna secara langsung pada request untuk memudahkan pengujian izin. Cara ini melewati proses autentikasi sesi yang   
    biasa digunakan browser. Karena hal itu, tes dengan `force_authenticate` saja tidak membuktikan bahwa pemeriksaan CSRF pada `SessionAuthentication` berjalan. Untuk mengujinya, proyek menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`. Tes kemudian akan mengirim POST tanpa token CSRF, memeriksa respons 403, dan memastikan data baru tidak tersimpan di database.

### AI Disclosure 

1. Tools AI yang Digunakan

* **Generative AI Tool:** Gemini 
* **Penggunaan Utama:** Membantu memahami penerapan Django REST Framework pada bagian Experience, termasuk serializer, permission, API view, URL, integrasi 
  frontend menggunakan `fetch()` serta memeriksa penyebab terjadinya error.


2. Strategi Prompting

* **Context-First Prompting:** Memberikan konteks lengkap file `views.py`, `forms.py`, dan serta isi lengkap folder main serta menjelaskan konteks tujuan 
  yang ingin dicapai sebelum meminta evaluasi perbaikan atau optimasi kode.
* **Constraint-Based Prompting:** Memberikan batasan bahwa pengerjaan harus mengikuti checklist minimal tugas, menggunakan model Experience yang
  sudah ada, serta memberikan arahan berdasarkan modul/bagian yang sedang dikerjakan.
* **Verify before execute:** Meminta AI memeriksa penyebab error sebelum menerapkan perbaikan. Setelah itu, kode diuji menggunakan command tests dan fitur 
serta fungsi CRUD dicoba kembali melalui localhost untuk memastikan tidak ada kesalahan.

3. Analisis Kritis Keterbatasan AI & Perbaikan Manual

* **Tes Lama Masih Menggunakan Endpoint Sebelumnya:** Panduan awal dari AI mengarahkan halaman Experience untuk menggunakan endpoint DRF baru, tetapi
  belum menyertakan perubahan pada tes lama yang masih mencari URL `/experience/json/`.
  **Perbaikan Manual:** Memperbarui `test_experience_page` di `main/tests.py` agar memeriksa `reverse("api:experience-list")`, kemudian
  menjalankan kembali `python manage.py test main` untuk double check.

* **Posisi Kode Tombol Edit:** Pada panduan AI, kode untuk menambahkan tombol Edit sempat diletakkan sebelum elemen `.project-actions` terbentuk.
  Akibatnya, halaman menampilkan pesan gagal memuat data ketika pengguna yang memiliki akses edit membuka daftar Experience.
  **Perbaikan Manual:** Memindahkan kode pembuatan tombol Edit ke setelah `article.innerHTML` dan sebelum `return article`, sehingga elemen tujuan
  sudah tersedia ketika tombol ditambahkan.

* **Pesan Validasi Kurang Sederhana:** Respons validasi dari API sempat ditampilkan bersama nama field, misalnya `ended_at:`, sehingga pesan toast
  seperti kurang intuitif bagi user.
  **Perbaikan Manual:** Memperbarui fungsi `apiErrorText` agar mengambil isi pesan dari respons API tanpa menampilkan nama field.

4. Log / Bukti Prompting

> *Daftar ringkasan prompt/interaksi utama dengan AI:*
> - **Pengguna:** *"Bagaimana alur implementasi serializer, permission, dan API view yang tepat agar sesuai dengan ketentuan minimal checklist pada tugas saya"*
> - **Pengguna:** *"Mengapa tombol Edit perlu ditambahkan setelah elemen `project-actions` dibuat di halaman?"*
> - **Pengguna:** *"Setelah menjalankan test, ternyata tes pada bagian `test_experience_page` error. Bagian apa yang perlu saya perbaiki dan mengapa tes masih mencari URL tersebut padahal halaman sudah menggunakan API yang baru? "*

### Tugas 7

1. Jelaskan apa yang dimaksud dengan widget tree pada Flutter dan bagaimana hubungan induk-anak (parent-child) bekerja antar-widget!

  Widget tree adalah struktur hierarkis di Flutter yang menggambarkan bagaimana widget-widget disusun dan saling terikat untuk membentuk tampilan antarmuka aplikasi. Hubungan parent-child disini bekerja dengan cara widget parent membungkus serta mengatur tata letak widget anak di dalamnya melalui properti seperti child atau children. Melalui struktur ini, widget induk dapat mewariskan sifat, ukuran, serta batasan tata letak kepada widget-widget child yang ada di bawahnya.

2. Sebutkan semua widget yang kamu gunakan dalam proyek ini dan jelaskan fungsinya masing-masing!

  **MaterialApp** 
  Berfungsi sebagai pengatur inti aplikasi berbasis Material Design, yang mengonfigurasi tema global, judul, serta halaman awal aplikasi.

  **Scaffold** 
  Menyediakan kerangka dasar tata letak visual halaman (seperti penyediaan AppBar di bagian atas dan body untuk isi konten utama).

  **AppBar** 
  Menampilkan bar navigasi atau header di bagian atas layar lengkap dengan judul dan warna tema.

  **SingleChildScrollView**
  Membuat konten di dalam layar dapat digulir (scrolled) secara vertikal untuk mencegah terjadinya error luapan piksel (overflow).

  **Padding**
  Memberikan jarak atau ruang kosong (margin internal) di sekeliling widget anak agar tidak menepi langsung ke batas layar.

  **Column & Row**
  Column berfungsi menyusun widget anak secara vertikal (atas ke bawah), sedangkan Row menyusun widget anak secara horizontal (kiri ke kanan).

  **Center**
  Berfungsi untuk menengahkan widget anak di dalamnya secara horizontal dan vertikal terhadap ruang yang tersedia.

  **SizedBox**
  Memberikan jarak kosong dengan ukuran tetap (fixed spacing) yang spesifik antara satu widget dengan widget lainnya.

  **InfoCard & ItemCard**
  Widget kustom buatan sendiri untuk menampilkan kartu informasi data diri serta tombol menu interaktif secara modular.

  **GridView.count**
  Menyusun daftar item menu dalam bentuk tata letak kisi (grid) dengan jumlah kolom tetap secara rapi.

3. Apa fungsi dari widget MaterialApp? Jelaskan mengapa widget ini umumnya digunakan sebagai root widget pada aplikasi Flutter!

  Widget ini berfungsi sebagai pengatur utama aplikasi yang menerapkan standar desain Google (Material Design). Di dalamnya, MaterialApp mengkonfigurasi berbagai elemen utama seperti tema warna global, judul aplikasi, halaman awal (home), serta sistem navigasi untuk berpindah antarhalaman.

  **Alasan digunakan sebagai Root Widget**
  Widget ini biasanya diletakkan sebagai root dari widget tree agar seluruh komponen atau halaman turunannya dapat mengakses konfigurasi, tema, dan navigasi secara konsisten. Tanpa MaterialApp di root, widget-widget standar Flutter tidak akan memiliki fondasi dasar yang diperlukan untuk merender tampilannya dengan benar.

4. Jelaskan perbedaan antara StatelessWidget dan StatefulWidget! Kapan kita sebaiknya memilih StatelessWidget dan kapan harus menggunakan StatefulWidget?

  StatelessWidget adalah widget yang bersifat statis atau immutable, artinya tampilannya tidak akan berubah setelah dirender karena tidak memiliki data internal (state). Sebaliknya, StatefulWidget adalah widget yang bersifat dinamis karena memiliki state terpisah yang dapat diperbarui sewaktu-waktu, sehingga bisa mengubah tampilan antarmuka secara otomatis lewat fungsi setState().

  **Kapan memilih masing-masing widget**
  Kita sebaiknya memilih StatelessWidget ketika membuat komponen yang sifatnya tetap dan tidak membutuhkan interaksi yang mengubah data internal (seperti teks statis, icon, atau kartu identitas). Di sisi lain, kita harus menggunakan StatefulWidget saat membangun komponen yang interaktif atau mengalami perubahan data secara berkala (seperti formulir input, tombol counter, animasi, atau status loading).

5. Apa itu BuildContext dan mengapa penting di Flutter? Bagaimana penggunaannya di dalam metode build?

  BuildContext adalah objek yang merepresentasikan lokasi sebuah widget di dalam struktur widget tree. Objek ini sangat penting karena memungkinkan sebuah widget mengetahui posisinya serta mengakses informasi global atau fitur dari widget-widget terdahulu (parent), seperti tema warna, media query, dan sistem navigasi.

  Dalam penggunaannya, parameter context selalu diterima di dalam metode build(BuildContext context). Parameter ini kemudian diteruskan ke fungsi bawaan seperti Theme.of(context) untuk mengambil gaya tema, atau digunakan saat melakukan navigasi dan menampilkan SnackBar.


6. Jelaskan konsep hot reload di Flutter dan apa perbedaannya dengan hot restart! Kapan kita tidak bisa hanya mengandalkan hot reload dan harus melakukan   hot restart atau full restart?
  
  Hot reload bekerja dengan cara menyisupkan perubahan kode yang baru saja diperbarui ke dalam Dart Virtual Machine yang sedang berjalan tanpa menghilangkan status aplikasi saat ini, sehingga reloadnya sangat cepat. Sebaliknya, hot restart memuat ulang seluruh aplikasi dari titik awal (main()), yang berarti seluruh status atau state aplikasi akan terhapus dan dimuat kembali dari kondisi awal.

  **Kapan digunakan**
  Kita tidak bisa selalu mengandalkan hot reload. Hot reload bisa digunakan jika kita menyisip atau mengubah kode tanpa mengganggu struktur utamanya, tetapi kita wajib melakukan hot restart atau full restart jika kita melakukan perubahan struktural tertentu seperti memodifikasi fungsi main(), mengubah nilai variabel global, menambah aset baru seperti gambar atau font, dan maupun mengubah inisialisasi awal aplikasi yang tidak dapat dibaca ulang oleh mesin virtual secara instan. Full restart sebenarnya dipakai jika terjadi perubahan kode native (seperti konfigurasi Android atau penambahan dependencies baru) yang tidak dapat ditangani oleh hot reload maupun hot restart.

### AI Disclosure 

1. Tools AI yang Digunakan

* **Generative AI Tool:** Gemini 
* **Penggunaan Utama:**  Membantu memahami tugas dan materi, memeriksa kode Flutter, menjelaskan penyebab serta letak error, dan membantu menyusun unit
test.

2. Strategi Prompting

* **Context-First Prompting:** Memberikan konteks dari tugas agar bisa memahami tujuang yang ingin dicapai
* **Constraint-Based Prompting:** Memberikan batasan scope yang dikerjakan sesuai dengan checklist minimal yang diinginkan soal
* **Verify before execute:**  Meminta penjelasan penyebab error sebelum melakukan perbaikan, serta memeriksa kembali hasilnya melalui aplikasi
  dan perintah pemeriksaan Flutter.

3. Analisis Kritis Keterbatasan AI & Perbaikan Manual

* **Tata Letak Belum Teruji pada Ukuran Layar Berbeda:** Pemeriksaan awal AI berfokus pada kesesuaian kode dengan checklist dan belum menjalankan
  aplikasi. Ketika aplikasi dibuka pada browser lebar, ukuran kartu membesar dan muncul pesan bottom overflow.
  **Perbaikan Manual:** Membungkus isi halaman menggunakan `SingleChildScrollView` dan membatasi tinggi kartu melalui `mainAxisExtent`
  pada `GridView.count`.

* **Kesalahan Penempatan Kurung saat Mengubah Widget Tree:** Saat menambahkan widget pembungkus, penutup daftar `children` pada `Column` utama sempat
  terlewat sehingga kode memiliki syntax error.
  **Perbaikan Manual:** Memeriksa kembali pasangan kurung dan susunan widget, lalu memperbaiki penutup `children`, `Column`,
  `Padding`, dan `SingleChildScrollView`.

* **Tes Bawaan Tidak Sesuai dengan Aplikasi:** Tes bawaan Flutter masih mencari angka counter `0`, sedangkan aplikasi sudah menampilkan halaman
  portofolio.
  **Perbaikan Manual:** Melakukan penyesuaian pada unit test agar memeriksa kartu identitas, tiga menu, dan pesan SnackBar sesuai fungsi aplikasi saat ini lalu diuji melalui perintah fultter test

4. Log / Bukti Prompting

> *Daftar ringkasan prompt/interaksi utama dengan AI:*
> - **Pengguna:** *"Setelah menambahkan SingleChildScrollView, apakah susunan kurung pada widget tree yang saya perbaiki sudah benar?"*
> - **Pengguna:** *"Mengapa muncul garis kuning-hitam dengan pesan bottom overflow pada halaman Flutter, coba jelaskan apa penyebabnya dan apa langkah     langkah mengatasinya?"*
> - **Pengguna:** *"Mengapa flutter test masih mencari teks 0 padahal aplikasi saya sudah berupa halaman portofolio, jelaskan apa maksud dan penyebabnya lalu berikan carfa untuk mengatasinya?"*