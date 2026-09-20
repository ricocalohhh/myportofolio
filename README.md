### Tugas 2

1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!

  - Efisiensi (DRY - Don't Repeat Yourself):`ModelForm` secara otomatis membangun input form berdasarkan field yang terdefinisi pada Model Django tanpa perlu menulis tag `<input>` secara manual di HTML.
  - Validasi Otomatis: Menangani validasi tipe data, batas karakter (`max_length`), serta status wajib isi (*required/blank*) di tingkat server, lalu mengembalikan pesan eror secara otomatis jika input tidak valid.
  - Kemudahan Penyimpanan: Memangkas proses *extract* data dari `request.POST` secara manual karena penyimpanan data ke database cukup dengan memanggil method `.save()`.

  Mengapa Diwajibkan Menambahkan `{% csrf_token %}`:
  - Digunakan untuk mencegah serangan CSRF (Cross-Site Request Forgery)
  * Tag ini menghasilkan token rahasia unik yang disisipkan sebagai *hidden input* pada form.
  * Saat form dikirimkan via metode `POST`, middleware Django memverifikasi token tersebut. Jika tidak cocok/tidak ada, Django menolak akses (`403 Forbidden`) untuk memastikan permintaan benar-benar berasal dari pengguna sah, bukan dari oknum berbahaya yang tak teridentifikasi

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
    
    - Ukuran Data Lebih Ringkas: JSON berbasis pasangan *key-value* tanpa tag pembuka/penutup yang tebal seperti pada XML `<item>value</item>`, sehingga menghemat konsumsi bandwidth dan mempercepat transfer data.
    - Integrasi Alami dengan JavaScript: JSON atau JavaScript Object Notation secara default didukung oleh JavaScript. Data dapat langsung diubah menjadi objek JavaScript menggunakan `.json()` pada Fetch API tanpa perlu parser khusus.
    - Keterbacaan (*Readability*): Strukturnya jauh lebih bersih, sederhana sehingga mudah dipahami oleh manusia.

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

    Alur Pengembalian Data Portofolio dalam Bentuk JSON:**
    - **HTTP Request:** browser mengirimkan permintaan `GET` ke endpoint API.
    - **Queryset Retrieval:** Fungsi *view* Django mengambil data dari database via ORM (contoh: `Projects.objects.all()`).
    - **Serialization:** Objek Python dikonversi menjadi format JSON menggunakan serializer Django atau `JsonResponse`.
    - **HTTP Response:** Klien menerima respon berformat `application/json`.

    Mengapa Perlu Melakukan Serialization:
    - Konversi Data: Serialization mengubah objek kompleks menjadi string teks standar (JSON) agar dapat dibaca, diproses, dan ditampilkan oleh ke user.

## AI Disclosure 

1. Tools AI yang Digunakan
* Generative AI Tool: Gemini AI
* Penggunaan Utama: Membantu menyusun layout CSS dan membantu memahami alur form serta membantu memahami kegunaan serta membuat file file_experience_delete dalam folder components, selain itu juga membantu memahami cara memakais postman walaupun saat dicoba belum berhasil

2. Strategi Prompting
* Context-First Prompting: Memberikan konteks penuh kode file Django (`views.py`, `models.py`, `experience.html`) dan aturan/konvensi proyek sebelum meminta solusi.
* Iterative & Constraint-Based Prompting: Menegaskan batasan khusus secara eksplisit, seperti "JANGAN menggunakan inline styles/hardcode style di tag HTML, gunakan class CSS eksternal", "Ubah dari Client-Side Rendering ke Server-Side Rendering (SSR)".
* Verify before execute: Sebelum AI mengeksekusi atau menulis ulang kode, instruksi diberikan untuk **menjelaskan penyebab masalah dan alur logika perubahan terlebih dahulu**. Hal saya lakukan untuk menghindari kesalahpahaman alur program, memastikan rencana perubahan sesuai dengan arsitektur Django (SSR), serta mencegah *refactoring* tak terduga yang merusak komponen HTML/CSS yang sudah rapi serta mempelajari penerapan teknis pada tiap langkah.

3. Analisis Kritis Keterbatasan AI & Perbaikan Manual
* Penanganan URL Pattern & Parameter Context: AI sempat menyarankan pemanggilan `{% include %}` tanpa meneruskan konteks variabel `with experience=item`, yang menyebabkan eror `NoReverseMatch` pada Django. 
**Perbaikan Manual:** Memperbaiki passing variabel context pada loop template Django secara manual.
* Kepatuhan Class CSS Internal: AI sempat menyusun elemen dengan class generik (`.btn`, `.btn-primary`) atau menyisipkan tag `<style>` inline. 
**Perbaikan Manual:** Menghapus seluruh tag `<style>` buatan AI dan menyelaraskan class HTML yang sudah ditulis (`.button`, `.project-header`, `.project-actions`).

4. Log / Bukti Prompting
> *Daftar ringkasan prompt/interaksi utama dengan AI disajikan dalam potongan di bawah:*
> - **User:** *"Mengapa experience tidak menggunakan django template rendering dan malah javascript? apakah bisa diubah?"*
> - **User:** *"Mengapa style disini, kan sudah diinstruksikan JANGAN HARDCODE"*
> - **User:** *"Hindari penggunaan tag `<style>` lokal maupun atribut `style` (inline CSS) secara langsung pada elemen HTML. Seluruh penataan tampilan wajib menggunakan kelas CSS dari berkas stylesheet eksternal."*

