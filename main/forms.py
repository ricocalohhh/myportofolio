from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, URLField
from django.core.exceptions import ValidationError  # TAMBAHKAN IMPORT INI
from django.utils.html import strip_tags           # TAMBAHKAN IMPORT INI

from django import forms
from django.utils.html import strip_tags
from main.models import Project, Experience

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'project_url', 'project_image_url']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return strip_tags(title) if title else title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return strip_tags(description) if description else description

    def clean_tech_stack(self):
        tech_stack = self.cleaned_data.get('tech_stack')
        return strip_tags(tech_stack) if tech_stack else tech_stack


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
