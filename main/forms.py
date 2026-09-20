from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, URLField

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "category",
            "description",
            "ended_at",
            "thumbnail",
        ]

        labels = {
            "title": "Judul / Posisi Pengalaman",
            "category": "Kategori",
            "description": "Deskripsi Pengalaman",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
            "thumbnail": "URL Gambar / Logo (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Asisten Dosen PBP",
                    "maxlength": 255,
                    "class": "form-control",
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Membantu mahasiswa...",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control custom-date",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                    "class": "form-control",
                }
            ),
        }