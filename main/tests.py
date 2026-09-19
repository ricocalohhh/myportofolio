from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
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
        
        # Karena rendering menggunakan AJAX/JS, periksa keberadaan ID container dan skrip fetch JSON
        self.assertContains(response, 'id="experience_cards"')
        self.assertContains(response, reverse("main:get_experience_json"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        """Menguji bahwa logika data selesai/berlangsung berfungsi dengan baik pada Endpoint JSON API"""
        self.experience.ended_at = timezone.now()
        self.experience.save()

        # Panggil endpoint JSON API 
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertEqual(response.status_code, 200)
        
        # Pastikan tanggal ended_at tidak null 
        self.assertNotContains(response, '"ended_at": null')

    def test_create_experience_view(self):
        """Menguji akses halaman form create dan proses pengiriman data baru"""
        get_response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(get_response.status_code, 200)

        # 2. Tes submit form penambahan data (POST)
        data = {
            "title": "Software Engineer Intern",
            "description": "Mengembangkan fitur aplikasi web.",
            "category": "internship",
        }
        post_response = self.client.post(reverse("main:create_experience"), data)
        
        # Memastikan berhasil 
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(Experience.objects.filter(title="Software Engineer Intern").exists())

    def test_edit_experience_view(self):
        """Menguji pembaruan data experience yang sudah ada"""
        edit_data = {
            "title": "Asisten Dosen PBP (Updated)",
            "description": "Membantu mahasiswa dan mengevaluasi tugas.",
            "category": "part-time",
        }
        response = self.client.post(
            reverse("main:edit_experience", kwargs={"id": self.experience.id}),
            edit_data,
        )

        # Memastikan berhasil 
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP (Updated)")

    def test_delete_experience_view(self):
        """Menguji penghapusan data experience"""
        response = self.client.get(
            reverse("main:delete_experience", kwargs={"id": self.experience.id})
        )

        # Memastikan berhasil 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 0)

    def test_get_experience_json_view(self):
        """Menguji pengembalian data dalam format JSON dan fitur filtering berdasarkan title"""
        # 1. Tes mengambil seluruh data JSON
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.experience.title)

        # 2. Tes filtering dengan query parameter   
        filter_response = self.client.get(
            reverse("main:get_experience_json") + "?title=Asisten"
        )
        self.assertEqual(filter_response.status_code, 200)
        self.assertContains(filter_response, "Asisten Dosen PBP")

        # 3. Tes filtering dengan query yang tidak cocok
        no_match_response = self.client.get(
            reverse("main:get_experience_json") + "?title=TidakAda"
        )
        self.assertNotContains(no_match_response, "Asisten Dosen PBP")

    def test_education_url_and_template(self):
        response = self.client.get('/education/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')

    def test_education_data_appears_when_exists(self):
        from main.models import Education
        Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            duration="2025 - Sekarang"
        )
        response = self.client.get('/education/')
        self.assertContains(response, "Universitas Indonesia")
        self.assertContains(response, "S1 Sistem Informasi")

    def test_education_empty_state_appears_when_no_data(self):
        response = self.client.get('/education/')
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

