from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from main.forms import ProjectForm, ExperienceForm, EducationForm
from main.models import Experience, Education, Project
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied 
from django.utils.html import strip_tags

from datetime import datetime


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Enrico Oscar Harits Caloh",
                "npm": "2506539990",
                "study_program": "S1 Sistem Informasi",
                "bio": (
                    "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
                    "pada proses bisnis dan teknologi."
                ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# ==================== SECTION PROJECTS ====================

def show_projects(request):
    context = {
        'name': request.user.username if request.user.is_authenticated else 'Visitor',
    }
    return render(request, "project.html", context) # Pastikan nama template sesuai, misal "projects.html" atau "project.html"

@login_required(login_url="/login/")
def create_project(request):
    # Hanya izinkan superuser
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }
    return render(request, "create_project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        # Indentasi diperbaiki: Masuk ke dalam loop for
        data.append({
            "id": str(project.id),
            "title": project.title,
            "description": project.description,
            "tech_stack": project.tech_stack,
            "project_url": project.project_url,
            "project_image_url": project.project_image_url,
            "star_count": starred_users.count(),
            "is_starred": is_starred,
            "starred_by_names": starred_by_names,
        })

    return JsonResponse(data, safe=False)

@login_required
def delete_project(request, id):
    # Validasi Hak Akses: Hanya superuser yang boleh menghapus
    if not request.user.is_superuser:
        return JsonResponse({'message': 'Akses Ditolak: Anda tidak memiliki izin.'}, status=403)

    if request.method == 'POST':
        project = get_object_or_404(Project, pk=id)
        project.delete()
        return JsonResponse({'message': 'Proyek berhasil dihapus!'}, status=200)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
            is_starred = False
        else:
            project.starred_by.add(request.user)
            is_starred = True

        return JsonResponse({
            "message": "Status star berhasil diperbarui.",
            "is_starred": is_starred,
            "star_count": project.starred_by.count(),
        }, status=200)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)

@login_required(login_url="/login/")
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# ==================== SECTION EXPERIENCE  ====================

# --- READ (Dapat diakses oleh SIAPA PUN: Anonymous, User, Editor, Superuser) ---

def show_experience(request):
    context = {
        'name': request.user.username if request.user.is_authenticated else 'Visitor',
    }
    return render(request, "experience.html", context)

# --- CREATE (Hanya Superuser) ---
@login_required(login_url="/login/")
@require_POST
def create_experience(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk menambah data."}, 
            status=403
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Berhasil menyimpan!"}, status=201)

    # Ambil pesan error pertama agar spesifik untuk Toast
    first_error = next(iter(form.errors.values()))[0] if form.errors else "Gagal menyimpan, periksa kembali input Anda."

    return JsonResponse(
        {
            "status": "error", 
            "message": first_error,
            "errors": form.errors.get_json_data()
        }, 
        status=400
    )

# --- EDIT / UPDATE (Hanya Editor/is_staff ATAU Superuser) ---
@login_required(login_url="/login/")
@require_POST
def edit_experience(request, id):
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk mengedit data ini."}, 
            status=403
        )

    try:
        experience = Experience.objects.get(pk=id)
    except Experience.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Data pengalaman tidak ditemukan."}, 
            status=404
        )

    form = ExperienceForm(request.POST, instance=experience)

    if form.is_valid():
        form.save()
        return JsonResponse(
            {"status": "success", "message": "Data pengalaman berhasil diperbarui!"}, 
            status=200
        )
    else:
        # Ambil pesan error pertama agar spesifik untuk Toast
        first_error = next(iter(form.errors.values()))[0] if form.errors else "Gagal memperbarui data. Periksa kembali input Anda."

        return JsonResponse(
            {
                "status": "error", 
                "message": first_error,
                "errors": form.errors.get_json_data()
            }, 
            status=400
        )

# --- DELETE ---
@login_required(login_url="/login/")
@require_POST
def delete_experience(request, id):
    # Sesuaikan dengan kebijakan role (apakah superuser saja atau termasuk staff)
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk menghapus data ini."}, 
            status=403
        )

    try:
        experience = Experience.objects.get(pk=id)
        experience.delete()
        return JsonResponse(
            {"status": "success", "message": "Pengalaman berhasil dihapus!"}, 
            status=200
        )
    except Experience.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Data pengalaman tidak ditemukan."}, 
            status=404
        )

@login_required(login_url="/login/")
@require_POST
def toggle_star_experience(request, experience_id): 
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
        is_starred = False
    else:
        experience.starred_by.add(request.user)
        is_starred = True

    return JsonResponse({
        "is_starred": is_starred,
        "star_count": experience.starred_by.count(),
        "starred_by_names": ", ".join([u.username for u in experience.starred_by.all()])
    })

# --- GET JSON ---
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        starred_users = exp.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "id": str(exp.id),
            "title": exp.title,
            "category": exp.category,
            "description": exp.description,
            "thumbnail": getattr(exp, "thumbnail", ""),
            "started_at": exp.started_at.strftime("%Y-%m-%d") if exp.started_at else None,
            "ended_at": exp.ended_at.strftime("%Y-%m-%d") if exp.ended_at else None,
            "star_count": starred_users.count(),
            "is_starred": is_starred,
            "starred_by_names": starred_by_names,
        })

    return JsonResponse(data, safe=False)

# ==================== SECTION EDUCATION ==================== 
def show_education(request):
    context = {
        'name': 'Enrico Oscar Harits Caloh',
        'npm': '2506539990',
        'study_program': 'S1 Sistem Informasi',
        'bio': 'Student in Information Systems with a strong focus on Finance, Business Development, Project Management, Product Management and Information Systems.',
    }
    return render(request, "education.html", context)

# Endpoint AJAX Get List Data JSON
def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    
    # Hapus prefetch_related('starred_by') di sini
    educations = Education.objects.all()

    if title_query:
        educations = educations.filter(institution__icontains=title_query)

    data = []
    for edu in educations:
        data.append({
            "id": str(edu.id),
            "institution": edu.institution,
            "degree": edu.degree,
            "field_of_study": getattr(edu, "field_of_study", ""),
            "description": getattr(edu, "description", ""),
            "started_at": edu.started_at.strftime("%Y-%m-%d") if hasattr(edu, "started_at") and edu.started_at else None,
            "ended_at": edu.ended_at.strftime("%Y-%m-%d") if hasattr(edu, "ended_at") and edu.ended_at else None,
        })

    return JsonResponse(data, safe=False)

# --- CREATE EDUCATION ---
@login_required(login_url="/login/")
@require_POST
def create_education(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk menambah data."}, 
            status=403
        )

    form = EducationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Pendidikan berhasil ditambahkan!"}, status=201)

    # Ambil pesan error spesifik pertama dari clean_<field>
    first_error = next(iter(form.errors.values()))[0] if form.errors else "Gagal menyimpan, periksa kembali input Anda."

    return JsonResponse(
        {
            "status": "error", 
            "message": first_error,
            "errors": form.errors.get_json_data()
        }, 
        status=400
    )

# --- EDIT EDUCATION ---
@login_required(login_url="/login/")
@require_POST
def edit_education(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk mengedit data ini."}, 
            status=403
        )

    try:
        education = Education.objects.get(pk=id)
    except Education.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Data pendidikan tidak ditemukan."}, 
            status=404
        )

    form = EducationForm(request.POST, instance=education)

    if form.is_valid():
        form.save()
        return JsonResponse(
            {"status": "success", "message": "Data pendidikan berhasil diperbarui!"}, 
            status=200
        )
    else:
        first_error = next(iter(form.errors.values()))[0] if form.errors else "Gagal memperbarui data."

        return JsonResponse(
            {
                "status": "error", 
                "message": first_error,
                "errors": form.errors.get_json_data()
            }, 
            status=400
        )

# --- DELETE EDUCATION ---
@login_required(login_url="/login/")
@require_POST
def delete_education(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk menghapus data ini."}, 
            status=403
        )

    try:
        education = Education.objects.get(pk=id)
        education.delete()
        return JsonResponse(
            {"status": "success", "message": "Data pendidikan berhasil dihapus!"}, 
            status=200
        )
    except Education.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Data pendidikan tidak ditemukan."}, 
            status=404
        )

# --- GET EDUCATION JSON ---
from django.http import JsonResponse
from .models import Education

def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.all()

    if title_query:
        educations = educations.filter(institution__icontains=title_query)

    data = []
    for edu in educations:
        start = edu.started_at.strftime('%Y') if hasattr(edu, 'started_at') and edu.started_at else ''
        end = edu.ended_at.strftime('%Y') if hasattr(edu, 'ended_at') and edu.ended_at else 'Present'
        
        if hasattr(edu, 'start_year') and edu.start_year:
            start = str(edu.start_year)
            end = str(edu.end_year) if edu.end_year else 'Present'

        duration = f"{start} - {end}" if start else getattr(edu, 'duration', '')

        data.append({
            'id': str(edu.id),
            'institution': edu.institution,
            'degree': edu.degree,
            'duration': duration,
            'logo_url': getattr(edu, 'logo_url', ''),
            'description': getattr(edu, 'description', ''),
        })

    return JsonResponse(data, safe=False)
