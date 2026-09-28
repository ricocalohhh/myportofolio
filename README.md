### Tugas 3

Deskripsi Proyek & Fitur Utama

- **Autentikasi & RBAC:** Fitur Register, Login, Logout dengan hak akses berbeda (Anonymous, Authenticated User, dan Superuser).
- **Fitur Interaktif Star:** Pengguna terautentikasi dapat memberikan/membatalkan *star* pada *Projects* dan *Experience* yang terhubung menggunakan relasi `ManyToManyField`.
- **Integritas API & Keamanan Data:** Endpoint JSON (`/api/projects/` dan `/experience/json/`) yang telah dibatasi menggunakan argumen `fields` pada serializer agar tidak membocorkan data sensitif pengguna (*hash password*, email, kredensial).

## AI Disclosure 

1. Tools AI yang Digunakan
* Generative AI Tool: Gemini AI
* Penggunaan Utama: Membantu mengatasi exception Django (related_name clash, NoReverseMatch), mengimplementasikan relasi ManyToManyField untuk fitur Star, serta mengamankan endpoint JSON dari risiko kebocoran data sensitif.

2. Strategi Prompting
* Context-First Prompting: Memberikan konteks penuh kode file Django (`views.py`, `models.py`, `experience.html`), serta memberi spesifikasi tugas sebelum meminta bantuan perbaikan.
* Iterative & Constraint-Based Prompting: Menegaskan batasan khusus secara eksplisit, seperti "Amankan endpoint JSON agar tidak membocorkan data sensitif user" dan "Gunakan Django Template Rendering untuk menampilkan data proyek dan star".
* Verify before execute: Meminta AI menjelaskan penyebab eror dan alur logikanya terlebih dahulu sebelum menuliskan ulang kode agar memahami penerapan teknis pada tiap langkah.

3. Analisis Kritis Keterbatasan AI & Perbaikan Manual
* Bentrokan Related Name ORM: AI awalnya merekomendasikan `ManyToManyField` tanpa related_name unik pada dua model berbeda (Project dan Experience), memicu error clash accessor.
**Perbaikan Manual:** Menambahkan `related_name="starred_projects"` dan `related_name="starred_experiences"` secara eksplisit pada models.py.
* Hilangnya Relasi M2M pada Deserialisasi JSON: Penggunaan `serializers.deserialize` buatan AI membuat objek kehilangan relasi live database sehingga tombol Star tidak muncul. 
**Perbaikan Manual:** Mengambil daftar ID dari hasil deserialisasi, lalu melakukan query ulang via `Project.objects.filter(pk__in=project_ids)` agar relasi `starred_by` tetap terbaca di template HTML.
* Kebocoran Data Sensitif pada JSON API: Secara default `serializers.serialize()` menyertakan seluruh atribut model dan relasi pengguna. 
**Perbaikan Manual:** embatasi output JSON menggunakan parameter `fields=(...)` pada `get_projects_json` dan `get_experience_json` untuk memastikan data sensitif pengguna tidak terekspos.

4. Log / Bukti Prompting
> *Daftar ringkasan prompt/interaksi utama dengan AI disajikan dalam potongan di bawah:*
> - **Pengguna:** *"Terjadi SystemCheckError terkait Reverse Accessor antara model Experience dan Project saat menjalankan makemigrations. Bagaimana cara menangani relasi many-to-many nya?"*
> - **Pengguna:** *"Pada fungsi show_projects di views.py terdapat logic penanganan JSON dari Tugas 3. Bagian ini mending dipertahankan atau dihapus? Gimana caranya supaya fitur star tetap berjalan aman?""*
> - **Pengguna:** *"Audit dan pastikan endpoint JSON API tetap berfungsi sesuai spesifikasi Tugas 3 tanpa mengekspos informasi sensitif pengguna."*

