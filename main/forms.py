from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, URLField
from django.core.exceptions import ValidationError  # TAMBAHKAN IMPORT INI
from django.utils.html import strip_tags           # TAMBAHKAN IMPORT INI

from django import forms
from django.utils.html import strip_tags
from main.models import Project, Experience, Education

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
            "started_at",
            "ended_at",
            "thumbnail",
        ]

        labels = {
            "title": "Judul / Posisi Pengalaman",
            "category": "Kategori",
            "description": "Deskripsi Pengalaman",
            "started_at": "Tanggal Mulai",
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
            "started_at": DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control custom-date",
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

    def clean(self):
           cleaned_data = super().clean()
           started_at = cleaned_data.get('started_at')
           ended_at = cleaned_data.get('ended_at')
   
           if started_at and ended_at and ended_at < started_at:
               raise ValidationError("Tanggal selesai tidak boleh lebih awal dari tanggal mulai.")
           
           return cleaned_data

    def clean_title(self):
        title = strip_tags(self.cleaned_data.get("title", "")).strip()
        if not title:
            raise ValidationError("Judul / posisi tidak boleh hanya berisi tag HTML.")
        return title

    def clean_category(self):
        return strip_tags(self.cleaned_data.get("category", "")).strip()

    def clean_description(self):
        description = strip_tags(self.cleaned_data.get("description", "")).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh hanya berisi tag HTML.")
        return description

    def clean_thumbnail(self):
        return strip_tags(self.cleaned_data.get("thumbnail", "")).strip()

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'duration', 'description', 'logo_url']
        # Sesuaikan 'fields' dengan nama kolom yang ada di model Education Anda

    def clean_institution(self):
        institution = strip_tags(self.cleaned_data.get("institution", "")).strip()
        if not institution:
            raise ValidationError("Nama institusi tidak boleh hanya berisi tag HTML atau kosong.")
        return institution

    def clean_degree(self):
        degree = strip_tags(self.cleaned_data.get("degree", "")).strip()
        if not degree:
            raise ValidationError("Gelar / jenjang tidak boleh hanya berisi tag HTML atau kosong.")
        return degree

    def clean_field_of_study(self):
        return strip_tags(self.cleaned_data.get("field_of_study", "")).strip()

    def clean_description(self):
        description = strip_tags(self.cleaned_data.get("description", "")).strip()
        return description

    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')

        # Jika model Anda menggunakan angka tahun atau tanggal untuk periode pendidikan
        if start_year and end_year and end_year < start_year:
            raise ValidationError("Tahun selesai tidak boleh lebih awal dari tahun mulai.")
        
        return cleaned_data
