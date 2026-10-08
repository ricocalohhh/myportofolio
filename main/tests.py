from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date
from main.models import Experience, Education
from django.contrib.auth.models import User

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2024, 1, 1),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        """Menguji bahwa halaman HTML mengembalikan template dan struktur JS yang benar"""
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        
        # UBAH BARIS INI: dari 'experience_cards' menjadi 'experience-grid-container'
        self.assertContains(response, 'id="experience-grid-container"')
        self.assertContains(response, reverse("main:get_experience_json"))

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditemukan.")

    def test_completed_experience(self):
        """Menguji bahwa logika data selesai/berlangsung berfungsi dengan baik pada Endpoint JSON API"""
        self.experience.ended_at = timezone.now().date()
        self.experience.save()

        response = self.client.get(reverse("main:get_experience_json"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '"ended_at": null')

    def test_education_url_and_template(self):
        response = self.client.get("/education/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears_when_exists(self):
        Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            duration="2022 - Present",
        )

        # Minta data melalui endpoint JSON AJAX
        response = self.client.get(reverse("main:get_education_json")) # Sesuaikan nama route JSON education kamu
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "S1 Sistem Informasi")

    def test_education_empty_state_appears_when_no_data(self):
        response = self.client.get("/education/")
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditemukan.")

class ExperienceAJAXTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Buat User Admin/Staff
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            email="admin@example.com",
            password="password123",
        )

        # 2. Buat User Biasa (Non-Staff)
        self.regular_user = User.objects.create_user(
            username="user_test",
            email="user@example.com",
            password="password123",
        )

        # 3. Buat Data Dummy untuk pengujian edit & search
        self.exp_dummy = Experience.objects.create(
            title="Asisten Dosen PBP",
            category="internship",
            description="Membantu kelas PBP",
            started_at="2024-01-01",
        )

    # --- 1. UJI STATUS HTTP 403 (FORBIDDEN) ---
    def test_create_experience_unauthorized(self):
        """User tanpa login -> 302 Redirect, User non-staff -> 403 Forbidden"""
        # Tanpa Login -> @login_required melakukan redirect (302)
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Hack Entry",
                "category": "full-time",
                "description": "Test",
                "started_at": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Login sebagai User Biasa (Non-Staff) -> Menghasilkan 403 Forbidden
        self.client.login(username="user_test", password="password123")
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Hack Entry",
                "category": "full-time",
                "description": "Test",
                "started_at": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 403)

        # Login sebagai User Biasa (Non-Staff)
        self.client.login(username="user_test", password="password123")
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Hack Entry",
                "category": "full-time",
                "description": "Test",
                "started_at": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 403)

    # --- 2. UJI STATUS HTTP 201 (CREATED) ---
    def test_create_experience_success(self):
        self.client.force_login(self.admin_user)
        
        data = {
            'title': 'Software Engineer Intern',
            'category': 'internship', 
            'description': 'Pengalaman membuat aplikasi web Django.',
            'started_at': '2023-01-01',  
            'ended_at': '2023-06-01', 
            'thumbnail': 'https://example.com/thumbnail.png',         
        }
        
        response = self.client.post(reverse('main:create_experience'), data)
        self.assertEqual(response.status_code, 201)

    # --- 3. UJI STATUS HTTP 400 (BAD REQUEST) ---
    def test_create_experience_invalid_form(self):
        """Admin membuat data TANPA started_at (Field Wajib) -> Harus 400 Bad Request"""
        self.client.login(username="admin_test", password="password123")

        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Invalid Entry",
                "category": "full-time",
                "description": "Tanpa tanggal mulai",
                "started_at": "",  # Kosong (Invalid)
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

    # --- 4. UJI STATUS HTTP 200 (OK) UNTUK EDIT ---
    def test_edit_experience_success(self):
        """Admin mengedit data yang ada -> Harus 200 OK"""
        self.client.login(username="admin_test", password="password123")

        url = reverse("main:edit_experience", args=[self.exp_dummy.id])
        response = self.client.post(
            url,
            {
                "title": "Asisten Dosen PBP (Updated)",
                "category": "research",  
                "description": "Membantu kelas PBP dan riset",
                "started_at": "2024-01-01",
                "ended_at": "2024-06-01",
                "thumbnail": "https://example.com/thumbnail.png",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.exp_dummy.refresh_from_db()
        self.assertEqual(self.exp_dummy.title, "Asisten Dosen PBP (Updated)")

        self.assertEqual(response.status_code, 200)
        self.exp_dummy.refresh_from_db()
        self.assertEqual(self.exp_dummy.title, "Asisten Dosen PBP (Updated)")

    # --- 5. UJI API SEARCH JSON ---
    def test_get_experience_json_search(self):
        """Uji endpoint pencarian AJAX"""
        response = self.client.get(
            reverse("main:get_experience_json") + "?title=Asisten"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Asisten Dosen PBP")