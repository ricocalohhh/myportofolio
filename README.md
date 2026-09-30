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

